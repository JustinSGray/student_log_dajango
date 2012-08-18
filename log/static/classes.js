//////////////////////
// Models
//////////////////////

Class = Backbone.Model.extend({
    defaults: {
    	name:"Class",
    	date:"08-11-2012",
    	active:true,
    },
});

Classes = Backbone.Collection.extend({
	model: Class,
});

//////////////////////
// Views
//////////////////////

ClassView = Backbone.View.extend({
	tagName: "tr",
	row_template: Handlebars.compile('<td>{{name}}</td><td>{{date}}</td>'),
	render:function(){
		//console.log(this.model.toJSON());
		var row = this.row_template(this.model.toJSON());
		this.$el.empty();
		this.$el.html(row);
		return this;
	},
});

ClassesView = Backbone.View.extend({
	tagName:"table",
	className:"table table-striped table-bordered",

	initialize: function(){
		this.collection = new Classes([new Class(), new Class(), new Class()])
		this.render();
	},
	render: function(){
        var self = this;
        _(self.collection.models).each(function(klass){
        	console.log(klass);
        	var cv = new ClassView({'model':klass});
        	self.$el.append(cv.render().el);
        });
        return self
	},
});

//////////////////////
// Main App
//////////////////////
var classes_view = new ClassesView;
$('#active_classes').append(classes_view.el)
