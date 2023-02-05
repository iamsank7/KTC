'use strict';
const router = require('express').Router();

router.get('/meta_wa_callbackurl', (req, res) => {
    const verify_token = process.env.Meta_WA_VerifyToken;

  // Parse params from the webhook verification request
  let mode = req.query["hub.mode"];
  let token = req.query["hub.verify_token"];
  let challenge = req.query["hub.challenge"];

  // Check if a token and mode were sent
  if (mode && token) {
    // Check the mode and token sent are correct
    if (mode === "subscribe" && token === Meta_WA_VerifyToken) {
      // Respond with 200 OK and challenge token from the request
      console.log("WEBHOOK_VERIFIED");
      res.status(200).send(challenge);
    } else {
      // Responds with '403 Forbidden' if verify tokens do not match
      res.sendStatus(403);
    }
  }
});

router.post('/meta_wa_callbackurl', async (req, res) => {
    try {
        console.log('POST: Someone is pinging me!');
        return res.sendStatus(200);
    } catch (error) {
                console.error({error})
        return res.sendStatus(500);
    }
});
module.exports = router;