const mongoose = require('mongoose')
const C = require("../constants.js")


mongoose.connect(C.MONGODB_URL, {
    useNewUrlParser: true,
    useCreateIndex: true,
    useUnifiedTopology: true,
    useFindAndModify: true
})
