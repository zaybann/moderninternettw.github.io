const request = require('request');

const options = {
  method: 'GET',
  url: 'https://myanmar-all-in-one-2d-results.p.rapidapi.com/api/v1/live',
  headers: {
    'X-RapidAPI-Key': 'eb32ae04f6mshc0184d8acb0899cp18bfc6jsnef066a8a98b3',
    'X-RapidAPI-Host': 'myanmar-all-in-one-2d-results.p.rapidapi.com'
  }
};

request(options, function (error, response, body) {
	if (error) throw new Error(error);

	console.log(body);
});
