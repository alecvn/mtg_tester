$(function() {

    $("div.card").hover(function() {
	var card_name = this.innerHTML;

	$(this).css({"color": "green"});
	card_name = card_name.split("+");

	if (card_name.length > 1) {
	  var new_card_name = "";
	  for (i in card_name) {
	    new_card_name += card_name[i];
	  }
	  card_name = new_card_name;
	} else {
	  card_name = card_name[0];
	}

	$("#featured_card")[0].src = "../media/images/" + card_name + ".jpg";

    });

    $("div.card").mouseout(function() {
        $(this).css({"color": "black"});
    });

    // $.widget("helpers.card_context", {
    //   options: {
    //   },

    //   _create: function() {
    // 	var that = this;
    // 	this.card_actions = this.element.find("div.card_actions")[0];
    // 	this.element.bind('click', $.proxy(this._show_actions, that));
    // 	$(this.card_actions).find("select").bind('change', $.proxy(this._execute_action, that));

    //   },

    //   _execute_action: function(event, data) {
    // 	console.log(event.currentTarget.value);
    // 	this.element.appendTo($(".play tr"));
    //   },

    //   _show_actions: function() {
    //   	this._trigger("card_selected");
    //   	this.element.find("div.card_container").css({"border": "1px solid yellow"});
    //   	$(this.card_actions).show();
    //   }

    // });

    // $("td.card_container").card_context();

    // $(document).bind("card_contextcard_selected",
    //   $.proxy(function() {
    // 	$("div.card_actions").hide();
    // 	$("div.card_container").css({"border": "none"});
    //   })
    // );

    $("div.card_image").click(function() {
	if ($(this)[0].nextElementSibling.children[0].value == 'tap') {
	    $(this).toggleClass("rotated_img");
	}
    });

    do_card_action = function() {
//	console.log(this);
    };

});

function send_message(socket) {
  var msg = document.getElementById("msg").value;
  socket.send({action: "message", message: msg, channel: "my_channel"});
};

function broadcast_message(msg, idx) {
  var widget = $("#card" + "_" + idx.toString()).data("helpers-card_context");
  $(widget.element).css({"display": "block"});
  $(widget.element).appendTo($(".hand tr"));

};

function draw_card(socket) {
  socket.send({action: "message", message: "draw a card", channel: "my_channel"});
};