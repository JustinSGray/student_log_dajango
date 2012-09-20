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
        '<td><a class="btn deact_btn"><i class="icon-off"></i></a>'+
        '<a class="btn del_btn"><i class="icon-trash"></i></a></td>'),
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
        //this.collection = new Classes([new Class(), new Class(), new Class()])
        this.collection.bind('remove',this.render,this);
        this.collection.bind('change',this.render,this);
        this.collection.bind('add',this.render,this);
        this.render();
    },
    events: {
        'click .add_btn':'add',
    },
    render: function(){
        var self = this;
        self.$el.empty();
        self.$el.append('<thead><tr><th>Name</th><th>Date</th><th style="width:80px;"></th></tr><thead>')
        //console.log(self.collection); 
        _(self.collection.where({active:self.options.active})).each(function(klass){
            var cv = new ClassView({'model':klass});
            self.$el.append(cv.render().el);
        });
        self.$el.append('<tr><td colspan="2"><input type="text" name="class_name" style="width:80%;" '+
            'placeholder="Class Name"></td>'+
            '<td><a class="btn add_btn"><i class="icon-plus"></i></a></td></tr>');
        return self
    },
    add: function(){
        var self = this;
        var c_name = this.$("input[name='class_name']").val(); 
        var klass = new Class({name:c_name,active:true})
        this.collection.add(klass);
        this.render();
    },
});

//////////////////////
// Main App
//////////////////////
var all_classes = new Classes([new Class({active:true}), new Class({active:true}), new Class({active:false})])
var active_classes = new ClassesView({collection:all_classes,active:true});
var inactive_classes = new ClassesView({collection:all_classes,active:false});

$('#active_classes').append(active_classes.el)
$('#inactive_classes').append(inactive_classes.el)
