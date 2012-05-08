$(function(){

    var Item = Backbone.Model.extend({
        defaults: function() {
            return {
                ident: ""
            };
        },
    });

    var TwitterItem = Item.extend({
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

    var ItemList = Backbone.Collection.extend({
        model: TwitterItem,

        url: '/twitter-items',

        comparator: function(item) {
            return item.get('ident');
        },

        parse: function(response) {
            return response.twitter_items;
        }

    });

    var TwitterItems = new ItemList;

    var AppView = Backbone.View.extend({
        el: $('#sonar'),

        initialize: function() {
            this.jug = new Juggernaut();
            this.jug.subscribe('tweet-channel', this.addTwitterItem);

            TwitterItems.bind('add', this.addTwitterItemToView, this);
            TwitterItems.bind('reset', this.addTwitterItems, this);

            TwitterItems.fetch();
        },

        addTwitterItems: function() {
            TwitterItems.each(this.addTwitterItemToView);
        },

        addTwitterItem: function(tweet) {
            var item = new TwitterItem(tweet);
            TwitterItems.create(item);
        },

        addTwitterItemToView: function(item) {
            var view = new TwitterItemView({
                model: item,
                id: "tweet-" + item.get('ident')
            });
            var new_item = view.render().el;
            $('#items').append(new_item);
        }
    });

    var App = new AppView;

});
