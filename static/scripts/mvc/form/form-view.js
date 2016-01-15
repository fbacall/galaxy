define(["utils/utils","mvc/ui/ui-portlet","mvc/ui/ui-misc","mvc/form/form-section","mvc/form/form-data"],function(a,b,c,d,e){return Backbone.View.extend({initialize:function(b){this.options=a.merge(b,{initial_errors:!1,cls:"ui-portlet-limited",icon:""}),this.modal=parent.Galaxy&&parent.Galaxy.modal||new c.Modal.View,this.setElement("<div/>"),this.render()},update:function(a){var b=this;this.data.matchModel(a,function(a,c){var d=b.input_list[a];if(d&&d.options&&!_.isEqual(d.options,c.options)){d.options=c.options;var e=b.field_list[a];if(e.update){var f=[];if(-1!=["data","data_collection","drill_down"].indexOf(d.type))f=d.options;else for(var g in c.options){var h=c.options[g];h.length>2&&f.push({label:h[0],value:h[1]})}e.update(f),e.trigger("change"),Galaxy.emit.debug("form-view::update()","Updating options for "+a)}}})},wait:function(a){for(var b in this.input_list){var c=this.field_list[b],d=this.input_list[b];d.is_dynamic&&c.wait&&c.unwait&&(a?c.wait():c.unwait())}},highlight:function(a,b,c){var d=this.element_list[a];if(d&&(d.error(b||"Please verify this parameter."),this.trigger("expand",a),!c))if(self==top){var e=this.$el.parents().filter(function(){return"auto"==$(this).css("overflow")}).first();e.animate({scrollTop:e.scrollTop()+d.$el.offset().top-50},500)}else $("html, body").animate({scrollTop:d.$el.offset().top-20},500)},errors:function(a){if(this.trigger("reset"),a&&a.errors){var b=this.data.matchResponse(a.errors);for(var c in this.element_list){{this.element_list[c]}b[c]&&this.highlight(c,b[c],!0)}}},render:function(){var a=this;this.off("change"),this.off("reset"),this.field_list={},this.input_list={},this.element_list={},this.data=new e.Manager(this),this._renderForm(),this.data.create(),this.options.initial_errors&&this.errors(this.options);var b=this.data.checksum();return this.on("change",function(){var c=a.data.checksum();c!=b&&(b=c,a.options.onchange&&a.options.onchange())}),this.on("reset",function(){for(var a in this.element_list)this.element_list[a].reset()}),this},_renderForm:function(){this.message=new c.Message,this.section=new d.View(this,{inputs:this.options.inputs}),$(".tooltip").remove(),this.portlet=new b.View({icon:this.options.icon,title:this.options.title,cls:this.options.cls,operations:this.options.operations,buttons:this.options.buttons,collapsible:this.options.collapsible,collapsed:this.options.collapsed}),this.portlet.append(this.message.$el),this.portlet.append(this.section.$el),this.$el.empty(),this.$el.append(this.portlet.$el),this.options.message&&this.message.update({persistent:!0,status:"warning",message:this.options.message}),Galaxy.emit.debug("form-view::initialize()","Completed")}})});
//# sourceMappingURL=../../../maps/mvc/form/form-view.js.map