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
      '<div class="modal-header">\
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>\
        <h4>{{title}}</h4>\
      </div>\
      <div class="modal-body">\
          {{&content}}\
      </div>\
      <div class="modal-footer">\
        <a href="#close" class="btn">Close</a>\
        <a href="#save" class="btn btn-primary">Save changes</a>\
      </div>';

    var searchItem = 
      '<form class="form-search">\
        <input type="text" class="input-medium search-query" id="q">\
        <button type="submit" class="btn">Search</button>\
       </form>';

    return {
      indexItem: indexItem,
      newsItem: newsItem,
      searchForm: searchItem
    };
  }

);
