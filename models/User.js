const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
  firstName: String,
  lastName: String,
  email: String,
  mobileNumber: String,
  password: String,
  confirm: String,
});

const User = mongoose.model('User_info', userSchema,'User_info');

module.exports = User;
