const mongoose = require('mongoose')

mongoose.connect('mongodb+srv://jobs:f4Uo1b3ziIAhpPMf@cluster0-79fkx.mongodb.net/test?retryWrites=true&w=majority', {
    useNewUrlParser: true,
    useCreateIndex: true,
    useUnifiedTopology: true,
    useFindAndModify: true
})
