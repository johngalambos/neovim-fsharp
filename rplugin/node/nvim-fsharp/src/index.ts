import { spawn, ChildProcess } from 'child_process';
import { Neovim } from 'neovim';
import { createInterface } from 'readline';
import { EOL } from 'os';

var fsacHandle = null;

const getLogger = (nvim) => (msg:string): void => {};

const getServer = () => {
  if (fsacHandle) {
    return fsacHandle;
  }
  fsacHandle = startServer();
  return fsacHandle;
};

// when we open an FSharp file in vim
const onBufEnter = (nvim: Neovim) => {
  return () => {
    // const serverHandle = getServer();
    // nvim.command('echomsg "hello"');
    // console.log('unbufwrite4');
    // console.log('starting the server');
    // serverHandle.stdin.write('help' + EOL);
    console.log('this should show up in the typescript log!');
    nvim.command('echomsg "I started the server"');
  };
};


const startServer = () => {

  let _rl: any;

  let serverHandle: ChildProcess = null;

  let _cwd = process.cwd();
  let _env = process.env;

  serverHandle = spawn(
    'dotnet',
    ['C:/Users/john/code/FsAutoComplete/src/FsAutoComplete.netcore/bin/Release/netcoreapp2.0/fsautocomplete.dll']
  );

  _rl = createInterface({
    input: serverHandle.stdout,
    output: serverHandle.stdin,
    terminal: false
  });

  _rl.on('line', msg => {
    console.log(`line event: ${msg}`);
    // if (msg.indexOf('{') === 0) {
    //   parseResponse(msg);
    // }
  });

  serverHandle.stderr.on('data', (data, err) => {
    console.error('Error from server: ' + data);
  });

  serverHandle.on('error', data => {
    console.log(`error Event: ${data}`);
  });

  serverHandle.on('exit', data => {
    console.log(`exit Event: ${data}`);
  });

  serverHandle.on('close', data => {
    console.log(`Close Event: ${data}`);
  });
  return serverHandle;

};

export default (plugin) => {
  plugin.setOptions({
    dev: true
  });
  //things we want to know about
  // * when an fsharp file is 
  // ** opened
  // ** edited
  plugin.registerAutocmd('BufEnter', onBufEnter(plugin.nvim), { pattern: '*.fs' });
};




