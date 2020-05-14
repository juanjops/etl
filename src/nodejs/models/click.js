const mongoose = require("mongoose")

const click = mongoose.model("click", {

    click: {
        type: String
    }
})


module.exports = click