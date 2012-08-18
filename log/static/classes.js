//////////////////////
// Models
//////////////////////

Class = Backbone.Model.extend({
    default: {
    	name:"Class",
    	date:"08-11-2012",
    	ative:true,
    },
});

Classes = Backbone.Collection.extend({
	model: Class,
});


active_classes = Classes([new Class, new Class, new Class])