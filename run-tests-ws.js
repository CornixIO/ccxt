// ----------------------------------------------------------------------------
// Usage: node run-tests [--php] [--js] [--python] [exchange] [symbol]

// ----------------------------------------------------------------------------

import fs from 'fs'
import ansi from 'ansicolor'
import log from 'ololog'
import {spawn} from 'child_process'
ansi.nice

// ----------------------------------------------------------------------------

const [,, ...args] = process.argv

const keys = {

    '--ts': false,      // run TypeScript tests only
    '--js': false,      // run JavaScript tests only
    '--php': false,     // run PHP tests only
    '--python': false,  // run Python 3 tests only
    '--python-async': false, // run Python 3 async tests only
}

let exchanges = []
let symbol = 'all'
let maxConcurrency = 5 // Number.MAX_VALUE // no limit

for (const arg of args) {
    if (arg.startsWith ('--'))               { keys[arg] = true }
    else if (arg.includes ('/'))             { symbol = arg }
    else if (Number.isFinite (Number (arg))) { maxConcurrency = Number (arg) }
    else                                     { exchanges.push (arg) }
}

// ----------------------------------------------------------------------------

if (!exchanges.length) {

    if (!fs.existsSync ('./exchanges.json')) {

        log.bright.red ('\n\tNo', 'exchanges.json'.white, 'found, please run', 'npm run build'.white, 'to generate it!\n')
        process.exit (1)
    }
    let exchangesFile =  fs.readFileSync('./exchanges.json');
    exchangesFile = JSON.parse(exchangesFile)
    exchanges = exchangesFile.ws
}

// ----------------------------------------------------------------------------

const sleep = s => new Promise (resolve => setTimeout (resolve, s))
const maxProcessTimeout = 300000 // 5 minutes

// ----------------------------------------------------------------------------

const exec = (bin, ...args) => {

    // a custom version of child_process.exec that captures both stdout and
    // stderr,  not separating them into distinct buffers — so that we can show
    // the same output as if it were running in a terminal.

    const ps = spawn (bin, args, { timeout: maxProcessTimeout })

    let output = ''
    let stderr = ''
    let hasWarnings = false

    ps.stdout.on ('data', data => { output += data.toString () })
    ps.stderr.on ('data', data => { output += data.toString (); stderr += data.toString (); hasWarnings = true })

    let return_
    const promise = new Promise ((resolve) => {
        return_ = resolve
    })

    ps.on ('exit', (code, signal) => {

        output = ansi.strip (output.trim ())
        stderr = ansi.strip (stderr)

        const regex = /\[[a-z]+?\]/gmi

        let match = undefined
        const warnings = []

        match = regex.exec (output)

        if (match) {
            warnings.push (match[0])
            do {
                if (match = regex.exec (output)) {
                    warnings.push (match[0])
                }
            } while (match);
        }

        return_ ({
            failed: code !== 0,
            stalled: (code === null) && (signal !== null),
            output,
            hasOutput: output.length > 0,
            hasWarnings: hasWarnings || warnings.length > 0,
            warnings: warnings,
        })
    })
    return promise
}

// ----------------------------------------------------------------------------

let numExchangesTested = 0

// tests of different languages for the same exchange should be run
// sequentially to prevent the interleaving nonces problem.

// ----------------------------------------------------------------------------

const sequentialMap = async (input, fn) => {

    const result = []
    for (const item of input) { result.push (await fn (item)) }
    return result
}

// ----------------------------------------------------------------------------

const testExchange = async (exchange) => {

    // run tests for all/selected languages (in parallel)

    const args = [exchange, ... (symbol === 'all') ? [] : [ symbol ]]
        , allTestsWithoutTs = [
            { language: 'JavaScript',     key: '--js',           exec: ['node',      'js/src/pro/test/test.js',           ...args] },
            { language: 'Python 3',       key: '--python',       exec: ['python3',   'python/ccxt/pro/test/test_async.py',       ...args] },
            { language: 'Python 3 Async', key: '--python-async', exec: ['python3',   'python/ccxt/pro/test/test_async.py',       ...args] },
            { language: 'PHP',            key: '--php',          exec: ['php', '-f', 'php/pro/test/test.php',         ...args] }
        ]
        , allTests = allTestsWithoutTs.concat([
            { language: 'TypeScript',     key: '--ts',           exec: ['node',  '--loader', 'ts-node/esm',  'ts/src/pro/test/test.ts',           ...args] },  
        ])
        , selectedTests  = allTests.filter (t => keys[t.key])
        , scheduledTests = selectedTests.length ? selectedTests : allTestsWithoutTs
        , completeTests  = await sequentialMap (scheduledTests, async test => Object.assign (test, await exec (...test.exec)))
        , failed         = completeTests.find (test => test.failed)
        , stalled        = completeTests.find (test => test.stalled)
        , hasWarnings    = completeTests.find (test => test.hasWarnings)
        , warnings       = completeTests.reduce ((total, { warnings }) => total.concat (warnings), [])

    // print interactive log output

    numExchangesTested++

    const percentsDone = ((numExchangesTested / exchanges.length) * 100).toFixed (0) + '%'

    let result
    if (stalled) {
        // a timeout is always also a fail
        result = 'TIMEOUT'.red
    } else if (failed) {
        result = 'FAILED'.red
    } else if (hasWarnings) {
        result = warnings.join (' ').yellow
    } else {
        result = 'OK'.green
    }

    const date = (new Date()).toISOString ()
    log.bright (date, ('[' + percentsDone + ']').dim, 'Testing WS', exchange.cyan, result)

    // return collected data to main loop

    return {

        exchange,
        failed,
        stalled,
        hasWarnings,
        explain () {
            for (const { language, failed, stalled, output, hasWarnings } of completeTests) {
                if (failed || hasWarnings) {

                    if (!failed && output.indexOf('[Skipped]') >= 0)
                        continue;

                    if (failed || stalled) { log.bright ((stalled ? '\nTIMEOUT' : '\nFAILED').bgBrightRed.white, exchange.red,    '(' + language + '):\n') }
                    else        { log.bright ('\nWARN'.yellow.inverse,      exchange.yellow, '(' + language + '):\n') }

                    log.indent (1) (output)
                }
            }
        }
    }
}

// ----------------------------------------------------------------------------

function TaskPool (maxConcurrency) {

    const pending = []
        , queue   = []

    let numActive = 0

    return {

        pending,

        run (task) {

            if (numActive >= maxConcurrency) { // queue task

                return new Promise (resolve => queue.push (() => this.run (task).then (resolve)))

            } else { // execute task

                let p = task ().then (x => {
                    numActive--
                    return (queue.length && (numActive < maxConcurrency))
                                ? queue.shift () ().then (() => x)
                                : x
                })
                numActive++
                pending.push (p)
                return p
            }
        }
    }
}

// ----------------------------------------------------------------------------

async function testAllExchanges () {

    const taskPool = TaskPool (maxConcurrency)
    const results = []

    for (const exchange of exchanges) {
        taskPool.run (() => testExchange (exchange).then (x => results.push (x)))
    }

    await Promise.all (taskPool.pending)

    return results
}

// ----------------------------------------------------------------------------

(async function () {

    log.bright.magenta.noPretty ('Testing'.white, Object.assign (
                                                            { exchanges, symbol, keys },
                                                            maxConcurrency >= Number.MAX_VALUE ? {} : { maxConcurrency }))

    const tested    = await testAllExchanges ()
        , warnings  = tested.filter (t => !t.failed && t.hasWarnings)
        , failed    = tested.filter (t =>  t.failed && !t.stalled)
        , stalled  = tested.filter (t =>  t.stalled)
        , succeeded = tested.filter (t => !t.failed && !t.hasWarnings)

    log.newline ()

    warnings.forEach (t => t.explain ())
    failed.forEach (t => t.explain ())

    log.newline ()

    if (failed.length)   { log.noPretty.bright.red    ('FAIL'.bgBrightRed.white, failed.map (t => t.exchange)) }
    if (stalled.length)  { log.noPretty.bright.red    ('TIMEOUT'.bgBrightRed.white, stalled.map (t => t.exchange)) }
    if (warnings.length) { log.noPretty.bright.yellow ('WARN'.inverse,           warnings.map (t => t.exchange)) }

    log.newline ()

    log.bright ('All done,', [failed.length    && (failed.length    + ' failed')   .red,
                              stalled.length   && (stalled.length + ' timed out').red,
                              succeeded.length && (succeeded.length + ' succeeded').green,
                              warnings.length  && (warnings.length  + ' warnings') .yellow].filter (s => s).join (', '))

    if (failed.length) {

        await sleep (10000) // to fight TravisCI log truncation issue, see https://github.com/travis-ci/travis-ci/issues/8189
        process.exit (1)

    } else {
        process.exit (0)
    }

}) ();

// ----------------------------------------------------------------------------
