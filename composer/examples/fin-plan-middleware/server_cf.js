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
    res.send({ 'Got it': 'Actual Cashflow summary on its way' })
})

router.get('/expected/:client', function (req, res, next) {
    console.log('Request URL:', req.originalUrl)
    console.log(req.params.client)
    res.send({ 'Got it': 'Expected Cashflow summary on its way' })
})

router.get('/realtime/:client', function (req, res, next) {
    console.log('Request URL:', req.originalUrl)
    console.log(req.params.client)
    res.send({'Got it':'Real-time Cashflow summary on its way'})
})

app.use('/cashflow/', router)
app.use(myLogger)
console.log('Cashflow Listening at port 9991')
app.listen(9991)
