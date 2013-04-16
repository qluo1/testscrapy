/*jslint node: true */
'use strict';
define(
  function() {
     var indexItem =
      '<table class="table">\
        <thead>\
          <tr>\
            <th> title </th>\
            <th> source </th>\
            <th> date </th>\
          </tr>\
        </thead>\
        <tbody>\
          {{#items}}\
            <tr>\
               <td><a href="#{{_id}}">{{title}}</a></td>\
               <td>{{source}}</td>\
               <td>{{date}}</td>\
            </tr>\
          {{/items}}\
        </tbody>\
       </table>';

    var newsItem = 
    '{{&content}}\
      <div class="modal-footer">\
        <button id="send_composed" disabled="disabled" class="btn btn-primary">Send</button>\
        <button id="cancel_composed" class="btn">Cancel</button>\
      </div>'
    ;

    return {
      indexItem: indexItem,
      newsItem: newsItem
    };
  }

);
