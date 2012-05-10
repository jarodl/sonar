$(function(){

    var Item = Backbone.Model.extend({
        set: function(attributes, options) {
            attributes['id'] = attributes['ident'];
            Backbone.Model.prototype.set.call(this, attributes, options);
        }
    });

    var TwitterItem = Item.extend({
    });

    var ItemView = Backbone.View.extend({
        tagName: "div",
    });

    var TwitterItemView = ItemView.extend({
        className: "twitter-item item",

        template: _.template($('#twitter-item').html()),

        initialize: function() {
            this.model.bind('change', this.render, this);
            this.model.bind('destroy', this.remove, this);
        },

        render: function() {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        },
    });

    var ItemList = Backbone.Collection.extend({
        model: TwitterItem,

        url: '/twitter/latest.json',

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
            var item = TwitterItems.get(tweet['ident']);
            if (!item) {
                item = new TwitterItem(tweet);
                TwitterItems.create(item);
            }
            else {
                item.set(tweet);
            }
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
