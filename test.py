import pyparsing as pp
report = '''
        Outstanding Issues Report - 1 Jan 2000

           # | Severity | Description                               |  Days Open
        -----+----------+-------------------------------------------+-----------
         101 | Critical | Intermittent system crash                 |          6
          94 | Cosmetic | Spelling error on Login ('log|n')         |         14
          79 | Minor    | System slow when running too many reports |         47
        '''
integer = pp.Word(pp.nums)
SEP = pp.Suppress('|')
# use SkipTo to simply match everything up until the next SEP
# - ignore quoted strings, so that a '|' character inside a quoted string does not match
# - parse action will call token.strip() for each matched token, i.e., the description body
string_data = pp.SkipTo(SEP, ignore=pp.quoted_string)
string_data.set_parse_action(pp.token_map(str.strip))
ticket_expr = (integer("issue_num") + SEP
              + string_data("sev") + SEP
              + string_data("desc") + SEP
              + integer("days_open"))

for tkt in ticket_expr.search_string(report):
    print(tkt.dump())