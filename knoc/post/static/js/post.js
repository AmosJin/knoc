var Group = Backbone.Collection.extend({
    url: '/api/post/group/',
    parse: function(response){
        return response.data;
    }

})

var Items = Backbone.Collection.extend({
    urlRoot: '/api/post/item/',
    parse: function(response){
        return response.data;
    }
})

var GroupView = Backbone.View.extend({
    el: 'groups',
    initialize: function(){
        self = this;
        this.collection.fetch({"success":function(collection){
                                self.render()}});
    },
    render: function(){
        var self = this;
        _.each(this.collection.models, function(model){
            $('#groups').append("<li>"+model.get("name") + "</li>");
        });
    }
})

var ItemView = Backbone.View.extend({
    className: "posts",
    initialize: function (){
        var page = self.options.get('page');
    }
})


new GroupView({collection:new Group()});
