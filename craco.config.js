module.exports = {
    webpack: {
      configure: {
        experiments: {
          topLevelAwait: true,
        },
      },
    },
    devServer: {
      headers: {
        "Access-Control-Allow-Origin": '"https://example.com", "http://localhost:3000", "https://webui.ipfs.io", "https://dev.webui.ipfs.io"',
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS",
        "Access-Control-Allow-Headers": "X-Requested-With, content-type, Authorization",
        "Access-Control-Allow-Credentials": "true"
      },
    }
    
  };