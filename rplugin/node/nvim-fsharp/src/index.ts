import { spawn, ChildProcess } from 'child_process';
import { createInterface } from 'readline';
import { EOL } from 'os';

const onBufWrite = (nvim) => {
  return () => {
    nvim.command('echomsg "hello"');
    console.log('unbufwrite4');
    console.log('starting the server');
    const serverHandle = startServer(nvim);
    serverHandle.stdin.write('help' + EOL);
    nvim.command('echomsg "I started the server"');
  };
};


const startServer = (nvim) => {

  let _rl: any;

  let serverHandle: ChildProcess = null;

  let _cwd = process.cwd();
  let _env = process.env;

  serverHandle = spawn(
    'dotnet',
    ['/Users/john/code/FsAutoComplete/bin/release_netcore/fsautocomplete.dll']
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
  console.log('initializing the plugin sucka2!!!');
  plugin.registerAutocmd('BufWritePre', onBufWrite(plugin.nvim), { pattern: '*' });
};




