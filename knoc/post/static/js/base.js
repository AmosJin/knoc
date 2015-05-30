var Group = Backbone.Model.extend({});

var Groups = Backbone.Collection.extend({
	model: Group,

    url: '/api/post/group/',

    parse: function(res){
        return res.data;
    }

})

var GroupView = Backbone.View.extend({
    el: '.groups',

    initialize: function(){
        this.groups = new Groups();
        this.groups.on("reset", this.render, this);
        this.groups.fetch({reset: true});
    },

    render: function(){
        var html = $("#groups-tmpl").tmpl({"groups": this.groups.toJSON()});
        this.$el.html(html);
    },
})

new GroupView();

$("#create-link").click(function(){
    $("#create-link-modal").modal({backdrop: 'static',});
});

$("#post-link").click(function(){
    $(".digest-list .item.shanbay").removeClass("hide");
});

$("#create-note").click(function(){
    var editor = new Simditor({
      textarea: $('#editor')
    })
    $(".content").addClass("create-note");
    $(".content>div").addClass("hide");
    $(".content .create-note-item").removeClass("hide");
});

$(".digest-list .item").click(function(e){
    $(".digest-list .item").removeClass('active');
    $(e.currentTarget).addClass('active');
    if($(e.currentTarget).hasClass("shanbay")){
        $(".content>div").addClass("hide");
        $(".content .shanbay-web").removeClass("hide");
        return;
    }
    $(".content>div").addClass("hide");
    $(".content .ngnix").removeClass("hide");
});
