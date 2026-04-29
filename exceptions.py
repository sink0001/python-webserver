class MalformedRequestLineError(Exception): pass
class MalformedHeaderError(Exception): pass
class RequestContinuityError(Exception): pass
class InvalidStatusCodeError(Exception): pass
class IllegalDuplicateHeaderError(Exception): pass