const express = require('express');
const router = express.Router();
const mongoose = require('mongoose');
const collections = require('./collections')

const surprise1 = collections[0];
const angry1 = collections[1];
const sad1 = collections[2];
const happy1 = collections[3];

router.get('/get', async (req, res) => {
  let all = [];
  for (let collection of collections) {
      let story = await collection.find();
      for (let item of story) {
          all.push(item);
      }
  }
  res.json(all);
})

module.exports = router;
