(function() {
    function splitOnWhitespace(trigger) {
      return trigger.split(/\s+/)
    }
  
    function parseClassOperation(trimmedValue) {
      var split = splitOnWhitespace(trimmedValue)
      if (split.length > 1) {
        var operation = split[0]
        var classDef = split[1].trim()
        var cssClass
        var delay
        if (classDef.indexOf(':') > 0) {
          var splitCssClass = classDef.split(':')
          cssClass = splitCssClass[0]
          delay = htmx.parseInterval(splitCssClass[1])
        } else {
          cssClass = classDef
          delay = 100
        }
        return {
          operation,
          cssClass,
          delay
        }
      } else {
        return null
      }
    }
  
    function performOperation(elt, classOperation, classList, currentRunTime) {
      setTimeout(function() {
        elt.classList[classOperation.operation].call(elt.classList, classOperation.cssClass)
      }, currentRunTime)
    }
  
    function toggleOperation(elt, classOperation, classList, currentRunTime) {
      setTimeout(function() {
        setInterval(function() {
          elt.classList[classOperation.operation].call(elt.classList, classOperation.cssClass)
        }, classOperation.delay)
      }, currentRunTime)
    }
  
    function processClassList(elt, classList) {
      var runs = classList.split('&')
      for (var i = 0; i < runs.length; i++) {
        var run = runs[i]
        var currentRunTime = 0
        var classOperations = run.split(',')
        for (var j = 0; j < classOperations.length; j++) {
          var value = classOperations[j]
          var trimmedValue = value.trim()
          var classOperation = parseClassOperation(trimmedValue)
          if (classOperation) {
            if (classOperation.operation === 'toggle') {
              toggleOperation(elt, classOperation, classList, currentRunTime)
              currentRunTime = currentRunTime + classOperation.delay
            } else {
              currentRunTime = currentRunTime + classOperation.delay
              performOperation(elt, classOperation, classList, currentRunTime)
            }
          }
        }
      }
    }
  
    function maybeProcessClasses(elt) {
      if (elt.getAttribute) {
        var classList = elt.getAttribute('classes') || elt.getAttribute('data-classes')
        if (classList) {
          processClassList(elt, classList)
        }
      }
    }
  
    htmx.defineExtension('class-tools', {
      onEvent: function(name, evt) {
        if (name === 'htmx:afterProcessNode') {
          var elt = evt.detail.elt
          maybeProcessClasses(elt)
          var classList = elt.getAttribute("apply-parent-classes") || elt.getAttribute("data-apply-parent-classes");
          if (classList) {
            var parent = elt.parentElement;
            parent.removeChild(elt);
            parent.setAttribute("classes", classList);
            maybeProcessClasses(parent);
          } else if (elt.querySelectorAll) {
            var children = elt.querySelectorAll('[classes], [data-classes]')
            for (var i = 0; i < children.length; i++) {
              maybeProcessClasses(children[i])
            }
          }
        }
      }
    })
  })()
  