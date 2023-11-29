

const mongoose = require('mongoose');

const storySchema = new mongoose.Schema({
    _id:Object,
    id: Number,
    title: String,
    story: String
  });
  
  const surprise = mongoose.model('surprise', storySchema,'surprise');
  const angry = mongoose.model('angry', storySchema,'angry');
  const sad = mongoose.model('sad', storySchema,'sad');
  const happy = mongoose.model('happy', storySchema,'happy');

  const collections = [surprise,angry,sad,happy]

  module.exports = collections