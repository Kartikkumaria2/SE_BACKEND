const express = require('express');
const router = express.Router();
const User = require('../models/User');

router.post('/info', async (req, res) => {
  try {
    // Destructure the data from the request body
    const { firstName, lastName, email, mobileNumber, password, confirm } = req.body;

    // Create a new User instance
    const newUser = new User({
      firstName,
      lastName,
      email,
      mobileNumber,
      password,
      confirm,
    });

    let user1 = await User.findOne({
      $or: [{ mobileNumber: mobileNumber }, { email: email }],
    });
    console.log(user1)
    if(!user1){
      const savedUser = await newUser.save();

      console.log('User saved to the database:', savedUser);
      res.status(201).json(savedUser); // Respond with the saved user data

    }
    else{
      console.log('enter unique values');
      res.status(500).json({message:"user already registered"})
    }

    
    
  } catch (error) {
    console.error('Error saving user to the database:', error);
    res.status(500).send('Internal Server Error');
  }
});


router.post('/login', async (req, res) => {
  try {
    const input1 = req.body.input1;
    const password = req.body.password;


    // Use Mongoose to find a user with the provided input1 in either the "mobile" or "email" column
    const user = await User.findOne({
      $or: [{ mobileNumber: input1 }, { email: input1 }],
    });


    if (!user) {
      console.log('not found');
      return res.status(404).json({ error: 'User not found' });
    }
    console.log(user);


    if (password != user.password) {
      console.log("here");
      return res.status(401).json({ error: 'Incorrect password' });
    }

    // If both input1 is found and the password is correct, you can proceed with your logic
    // For example, you might generate a JWT token for authentication

    res.status(200).json({ message: 'Login successful', user: user, success: true });
  } catch (error) {
    console.error('Error during login:', error);
    res.status(500).send('Internal server error');
  }
});
router.get('/login', (req, res) => {
  console.log(req.body);
})

module.exports = router;





