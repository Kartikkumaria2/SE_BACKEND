const express = require('express');
const app = express();
const port  =process.env.PORT || 3000;
const router = express.Router();
const mongoose = require('mongoose')
const cors = require('cors');
require('dotenv').config()


mongoose.connect(process.env.DATABASE_URL);

const db = mongoose.connection 
db.on('error',(error)=>console.error(error));
db.once('open',()=> console.log("connected to db"));

app.use(cors());

app.use(express.json());

const companyRouter = require('./routes/photos')
app.use('/photo',companyRouter);

const userRouter = require('./routes/user')
app.use('/user',userRouter)

const storyRouter = require('./routes/story')
app.use('/story',storyRouter)

const allRouter = require('./routes/fetcher')
app.use('/allstories',allRouter)

app.listen(port, () => {
    console.log(`Server running at http://127.0.0.1:${port}/`);
});