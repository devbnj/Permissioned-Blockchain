let express = require('express')
let app = express()
let router = express.Router()

var myLogger = function (req, res, next) {
    console.log('LOGGED')
    next()
}

router.use(function (req, res, next) {
    console.log('Time:', Date.now())
    next()
})

router.get('/actual/:client', function (req, res, next) {
    console.log('Request URL:', req.originalUrl)
    console.log(req.params.client)
    res.send({ 'Got it': 'Actual balance sheet summary on its way' })
})

router.get('/balance/:client', function (req, res, next) {
    console.log('Request URL:', req.originalUrl)
    console.log(req.params.client)
    res.send({ 'Got it': 'Balance sheet (balance) summary on its way' })
})

router.get('/liabilities/:client', function (req, res, next) {
    console.log('Request URL:', req.originalUrl)
    console.log(req.params.client)
    res.send({'Got it':'Balance sheet (liabilities) summary on its way'})
})

app.use('/balancesheet/', router)
app.use(myLogger)
console.log('Balancesheet Listening at port 9992')
app.listen(9992)
