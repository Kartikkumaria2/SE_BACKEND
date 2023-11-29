const express = require('express');
const router = express.Router();
const mongoose = require('mongoose');
const collections  = require('./collections')

const surprise = collections[0];
const angry = collections[1];
const sad = collections[2];
const happy = collections[3];


  
  router.post('/fetch', async (req, res) => {
    try {
      const x = await req.body.sent
      const emotion = String(x); // Assuming the emotion is sent in the request body
      console.log("emotion sent is:")
  
      // Determine the collection based on the emotion
      let StoryModel;
      switch (emotion.trim()) {
        case 'Surprise':
          StoryModel =   surprise
          break;
        case 'Angry':
          StoryModel = angry;
          break;
          case 'Sad':
          StoryModel = sad;
          break;

          case 'Happy':
          StoryModel = happy;
          break;
        
  
        default:
          StoryModel = angry;
          break;
      }
      const docCount = await StoryModel.countDocuments();
      console.log(docCount);
      // Retrieve all documents from the specified collection
      const allStories = await StoryModel.find();
      
      // Randomly select one story
      const randomIndex = Math.floor(Math.random() * allStories.length);
      const randomStory = allStories[randomIndex];

      console.log(allStories);
  
      // Send the title and story as the response
      res.json({
        title: randomStory.title,
        story: randomStory.story
      });
    } catch (error) {
      console.error('Error:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  });
  
  module.exports = router;
 
  
  
  
  
  
  

