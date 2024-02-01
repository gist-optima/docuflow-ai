def validate_container_structure(container):
    def test(container, depth=0):
        if depth > 3: 
            raise RecursionError("To deep")
        elif container is None:
            return
        elif isinstance(container, dict):
            if len(container.keys()) == 0:
                raise ValueError("Empty dictionary is not allowed!")
            for child in container.values():
                if child is not None:
                    test(child, depth=depth+1)
            return
        else:
            raise ValueError("Invalid structure")   
        
    try:
        test(container)
    except:
        return False
    else:
        return True


    