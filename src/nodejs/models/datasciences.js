const mongoose = require("mongoose")

const dataScience = mongoose.model("datasciences", {

    job_id: {type: String, required : true, trim: true},
    title: {type: String, trim: true},
    company: {type: String, trim: true},
    location: {type: String, trim: true},
    posted: {type: Date, default: Date.now}, 
    text: {type: String, trim: true},
    level: {type: String, trim: true},
    type: {type: String, trim: true},
    available: {type: String, trim: true, default: "Available"},
    target: {type: String, trim: true},
    link: {type: String}
    },
    "datasciences"
)

const dataScience_analysis = mongoose.model("datasciences_analysis", {

    job_id: {type: String,required : true,trim: true},
    key_words: {type: String,trim: true},
    misspelled_words: {type: String,trim: true},
    experience: {type: String,trim: true},
    ML: {type: Number},
    Math: {type: Number},
    BI: {type: Number},
    Big_D: {type: Number},
    CI_CD: {type: Number},
    Serv: {type: Number},
    Language: {type: String,trim: true},
    target: {type: String,trim: true},
    },
    "datasciences_analysis"
)

module.exports = {
    dataScience,
    dataScience_analysis
}