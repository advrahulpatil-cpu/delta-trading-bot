const crypto = require('crypto');

function generateDeltaSignature(secret, timestamp, method, path, body) {
  const payload = `${method}${timestamp}${path}${JSON.stringify(body)}`;
  return crypto.createHmac('sha256', secret).update(payload).digest('hex');
}

module.exports = generateDeltaSignature;
