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
	row_template: Handlebars.compile('<td><a href="">{{name}}</a></td><td>{{date}}</td>'+
		'<td><a class="btn del_btn"><i class="icon-trash"></i></a></td>'),
	events: {
		'click .del_btn':'clear'
	},
	initialize: function(){
		this.model.on('destroy',this.remove,this);
	},
	render:function(){
		var row = this.row_template(this.model.toJSON());
		this.$el.empty();
		this.$el.html(row);
		return this;
	},
	clear:function(){
		this.off();
		this.model.destroy();
	},

});

ClassesView = Backbone.View.extend({
	tagName:"table",
	className:"table table-striped table-bordered table-condensed",
	initialize: function(){
		this.collection = new Classes([new Class(), new Class(), new Class()])
		this.render();
	},
	active: false,
	render: function(){
        var self = this;
        self.$el.append('<thead><tr><th>Name</th><th>Date</th><th style="width:40px;"></th></tr><thead>')
        _(self.collection.models).each(function(klass){
        	var cv = new ClassView({'model':klass});
        	self.$el.append(cv.render().el);
        });
        self.$el.append('<tr><td colspan="2"><input type="text" name="class_name" style="width:80%;" placeholder="Class Name"></td>'+
        	'<td><a class="btn add_btn"><i class="icon-plus"></i></a></td></tr>');
        return self
	},
});

//////////////////////
// Main App
//////////////////////
var active_classes = new ClassesView({attributes:{'active':true}});
var inactive_classes = new ClassesView;

$('#active_classes').append(active_classes.el)
$('#inactive_classes').append(inactive_classes.el)
