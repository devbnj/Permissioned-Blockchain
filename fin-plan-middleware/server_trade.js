/*eslint-disable*/ 
/*jshint esversion: 6*/
let express = require('express');
let app = express();
let router = express.Router();

let tradeOrderEnum = {"PRELIMINARY":1, 
    "PROPOSED":2, "PRETRADE":3, 
    "NEWORDER":4, "PLACED":5, 
    "EXECUTED":6, "POSTTRADE":7 };
Object.freeze(tradeOrderEnum)

var myLogger = function (req, res, next) {
    console.log('LOGGED')
    next()
}

router.use(function (req, res, next) {
    console.log('Time:', Date.now())
    next()
})

router.get('/initiate/:ordertype/:client', function (req, res, next) {
    let orderType = req.params.ordertype;
    switch (orderType) {
        case (tradeOrderEnum.EXECUTED): // do something
        case (tradeOrderEnum.NEWORDER): // do something
        case (tradeOrderEnum.PLACED): // do something
        case (tradeOrderEnum.POSTTRADE): // do something
        case (tradeOrderEnum.PRELIMINARY): // do something
        case (tradeOrderEnum.PRETRADE) : // do something
        case (tradeOrderEnum.PROPOSED) : // do something
        default: break;
    }
    console.log('Request URL:', req.originalUrl)
    console.log(req.params.client, req.params.ordertype)
    res.send({ 'Got it': 'Trade order on its way' })
})

app.use('/tradeorder/', router)
app.use(myLogger)
console.log('Tradeorder Listening at port 9993')
app.listen(9993)
