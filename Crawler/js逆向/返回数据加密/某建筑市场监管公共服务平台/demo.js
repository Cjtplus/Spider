// 需要先下载crypto-js
// npm install crypto-js

const CryptoJS = require('crypto-js');

function decrypt(t) {
            var f = CryptoJS.enc.Utf8.parse("jo8j9wGw%6HbxfFn"),
            m = CryptoJS.enc.Utf8.parse("0123456789ABCDEF"),
            e = CryptoJS.enc.Hex.parse(t),
            n = CryptoJS.enc.Base64.stringify(e),
            a = CryptoJS.AES.decrypt(n, f,
            {
                iv: m,
                mode: CryptoJS.mode.CBC,
                padding: CryptoJS.pad.Pkcs7
            }),
            r = a.toString(CryptoJS.enc.Utf8);
            return r.toString()
        }