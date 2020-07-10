const mongoose = require("mongoose")

const twitter = mongoose.model("tweets", {

    id_str: {type: String, required : true, trim: true},
    text: {type: String, required : true, trim: true},
    screen_name: {type: String, required : true, trim: true},
    created_at: {type: String, required : true, trim: true}
    },
    "tweets"
)

module.exports = twitter