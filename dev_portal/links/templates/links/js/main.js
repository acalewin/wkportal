App = Ember.Application.create({
  LOG_TRANSITIONS: true,
});

App.Router.map(function() {
  this.route('kanjidetails', {path: '/kanji/:id'});

});

App.LinkModel = Ember.Object.extend({

});

App.KanjiModel = Ember.Object.extend({

});

App.LinkList = Ember.ArrayController.create([]);
App.KanjiList = Ember.ArrayController.create([]);

App.ApplicationController = Ember.Controller.extend({
  init: function() {
    // Get the Links
    $.getJSON("{% url 'links:list'%}", function(data) {
      $.each(data, function(idx, itm) {
        App.LinkList.pushObject(App.KanjiModel.create(itm.fields));
      })
    });
    // Get Kanji *counts* not the lists
  }
});

App.KanjiRoute = Ember.Controller.extend({
  setupController: function() {
    // Get the list of kanji now that we actually want to see them
  }
})

App.KanjiController = Ember.Controller.extend({
  status: '',
  actions: {
    pull_list: function() {

    },
    set_apikey: function() {

    }
  }
});

App.LinkListView = Ember.View.extend({
  templateName: 'linklist'
})
