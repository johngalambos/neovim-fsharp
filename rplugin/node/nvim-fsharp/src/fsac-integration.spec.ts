import { hello } from './index';
import { expect } from 'chai';
import 'mocha';

describe('fsac server', () => {

  var serverHandle;

  before(() => {
    console.log('starting the server');
  });

  it('should return hello world', () => {
    const result = hello();
    console.log('running the test');
    expect(result).to.equal('Hello World');
  });

  after(() => {
    console.log('stopping the server');
  });
});


