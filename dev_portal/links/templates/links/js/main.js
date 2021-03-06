
// TODO: Handle errors and display messages returned from the server

App = Ember.Application.create({
  LOG_TRANSITIONS: true,
});

App.Router.map(function() {
  this.route('kanjidetails', {path: '/kanji/:id'});
  this.route('gradesentence');
  this.route('listsentences');
});

App.LinkModel = Ember.Object.extend({

});

App.KanjiModel = Ember.Object.extend({

});

App.LinkList = Ember.ArrayController.create([]);
App.KanjiList = Ember.ArrayController.create([]);

App.CSRFToken = "{{ csrf_token }}";

App.ApplicationController = Ember.Controller.extend({
  init: function() {
    // Get the Links
    $.getJSON("{% url 'links:list'%}", function(data) {
      $.each(data, function(idx, itm) {
        App.LinkList.pushObject(App.KanjiModel.create(itm.fields));
      })
    });
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

App.GradesentenceController = Ember.Controller.extend({
  jptext: '',
  apikey: '',
  actions: {
    grade: function(){
      var self = this;
      $.post("{% url 'wanikani:gradekanji'%}",
        {sentence: self.get('jptext'),
        csrfmiddlewaretoken: App.get('CSRFToken'),
        apikey: self.get('apikey')},
        function(data) {
          self.set('graded_text', Ember.ArrayController.create());
          self.get('graded_text').pushObjects(data);
        });
    },
    savekey: function() {
      $.post("{% url 'wanikani:setkey'%}",
        {apikey: this.get('apikey'),
        csrfmiddlewaretoken: App.get('CSRFToken')},
        function(data) {
          alert('key saved!');
        })
    },
    savesentence: function() {
      $.post("{% url 'wanikani:savesentence'%}",
        {sentence: this.get('jptext'),
        csrfmiddlewaretoken: App.get('CSRFToken')},
        function(data) {
          alert('saved sentence!');
        })
    },
  }
});

App.ListsentencesRoute = Ember.Route.extend({
  model: function() {
    return Ember.$.getJSON("{% url 'wanikani:listsentences' %}");
  }
});

App.ListsentencesController = Ember.Controller.extend({

});
