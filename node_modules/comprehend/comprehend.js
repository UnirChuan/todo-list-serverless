
// Copyright 2018 Sleepless Inc. All Rights Reserved

module.exports = function (creds, str) {
	let ac = require('@datafire/amazonaws_comprehend').create(creds);
	return new Promise( (resolve, reject) => {
		var lc = null;
		var entities = null;
		var phrases = null;
		var sentiment = null;
		ac.DetectDominantLanguage({ "Text": str, })
		.then(data => {
			return data.Languages[0].LanguageCode;
		})
		.then(data => {
			lc = data;
			return ac.DetectEntities({ "Text": str, "LanguageCode": lc });
		})
		.then(data => {
			entities = data;
			return ac.DetectKeyPhrases({ "Text": str, "LanguageCode": lc });
		})
		.then(data => {
			phrases = data;
			return ac.DetectSentiment({ "Text": str, "LanguageCode": lc });
		})
		.then(data => {
			sentiment = data;
			return { lc: lc, entities: entities, phrases: phrases, sentiment: sentiment, };
		})
		.then(data => {
			resolve(data); 
		})
	});
};


