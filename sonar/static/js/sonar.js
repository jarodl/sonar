$(function(){

    var Item = Backbone.Model.extend({
        defaults: function() {
            return {
                ident: ""
            };
        },
    });

    var TwitterItem = Backbone.Model.extend({
        defaults: function() {
            return {
                object_id: "",
                image_url: "",
                text: ""
            };
        },

        // initialize: function(object_id, image_url, text) {
        //     this.set({
        //         "object_id": object_id, 
        //         "image_url": image_url,
        //         "text": text
        //     });
        // }
    });

    var ItemView = Backbone.View.extend({
        tagName: "div",
    });

    var TwitterItemView = Backbone.View.extend({

        tagName: "div",

        className: "twitter-item item",

        template: _.template($('#twitter-item').html()),

        initialize: function() {
            this.model.bind('change', this.render, this);
        },

        render: function() {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        },
    });

    var AppView = Backbone.View.extend({
        el: $('#sonar'),

        initialize: function() {
            this.jug = new Juggernaut();
            this.jug.subscribe('tweet-channel', this.addTwitterItem);
        },

        addTwitterItem: function(tweet) {
            var item = new TwitterItem(tweet);
            var view = new TwitterItemView({
                model: item,
                id: "tweet-" + item.object_id
            });
            var new_item = view.render().el;
            $('#items').append(new_item);
        },
    });

    var App = new AppView;

});
