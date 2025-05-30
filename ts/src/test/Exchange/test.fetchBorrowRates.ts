
import assert from 'assert';
import testBorrowRate from './base/test.borrowRate.js';

async function testFetchBorrowRates (exchange, skippedProperties) {
    const method = 'fetchBorrowRates';
    const borrowRates = await exchange.fetchBorrowRates ();
    assert (typeof borrowRates === 'object', exchange.id + ' ' + method + ' must return an object. ' + exchange.json (borrowRates));
    const values = Object.values (borrowRates);
    for (let i = 0; i < values.length; i++) {
        testBorrowRate (exchange, skippedProperties, method, values[i], undefined);
    }
}

export default testFetchBorrowRates;
