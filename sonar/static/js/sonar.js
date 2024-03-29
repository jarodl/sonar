$(function(){

    var Item = Backbone.Model.extend({
        set: function(attributes, options) {
            attributes['id'] = attributes['ident'];
            Backbone.Model.prototype.set.call(this, attributes, options);
        }
    });

    var LatestTweet = Item.extend({
    });

    var ItemView = Backbone.View.extend({
        tagName: "div",
    });

    var LatestTweetView = ItemView.extend({
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
        model: LatestTweet,

        url: '/twitter/latest.json',

        comparator: function(item) {
            return item.get('ident');
        },

        parse: function(response) {
            return response.latest_tweets;
        }
    });

    var LatestTweets = new ItemList;

    var AppView = Backbone.View.extend({
        el: $('#sonar'),

        initialize: function() {
            this.jug = new Juggernaut();
            this.jug.subscribe('tweet-channel', this.addLatestTweet);

            LatestTweets.bind('add', this.addLatestTweetToView, this);
            LatestTweets.bind('reset', this.addLatestTweets, this);

            LatestTweets.fetch();
        },

        addLatestTweets: function() {
            LatestTweets.each(this.addLatestTweetToView);
        },

        addLatestTweet: function(tweet) {
            var item = LatestTweets.get(tweet['ident']);
            if (!item) {
                item = new LatestTweet(tweet);
                LatestTweets.create(item);
            }
            else {
                item.set(tweet);
            }
        },

        addLatestTweetToView: function(item) {
            var view = new LatestTweetView({
                model: item,
                id: "tweet-" + item.get('ident')
            });
            var new_item = view.render().el;
            $('#items').append(new_item);
        }
    });

    var App = new AppView;

});
