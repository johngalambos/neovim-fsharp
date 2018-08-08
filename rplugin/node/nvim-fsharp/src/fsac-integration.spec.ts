import { sendHelp, cleanup } from './index';
import { expect } from 'chai';
import 'mocha';

describe('fsac server', () => {

  it('should return content from help', () => {
    console.log('running the test');
    sendHelp();
  });

  after(() => {
    console.log('stopping the server');
    cleanup();
  });
});


