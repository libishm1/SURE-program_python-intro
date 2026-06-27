# ============================================================
# CONCEPT: following DATAFLOW to find a bug (debugging lesson)
# ============================================================
# "Dataflow" = how a value is born, changes, and is used.
# This script has a DELIBERATE BUG. The goal of the lesson is to
# find it by watching the data move, not by guessing.
#
# Two ways to watch dataflow:
#   A) print-tracing  (the print() lines below)
#   B) the debugger   (set a breakpoint on the marked line, then
#      press F5 in VS Code and watch the variables panel)
#
# TASK FOR STUDENTS:
#   Run it. It CRASHES with ZeroDivisionError. But the division is
#   not the real problem -- it is where the bad data finally bites.
#   Use the trace (or a breakpoint) to see WHICH value is wrong and
#   WHERE it went wrong, then fix that ONE line.
# ============================================================

scores = [80, 90, 100]


def average(values):
    total = 0
    count = 0
    for v in values:
        total = total + v
        # count = count + 1     # <-- BUG: this line is commented out!
        # TRACE: watch total grow while count stays stuck at 0.
        print(f"  saw {v:3d} | running total = {total:3d} | count = {count}")
    print(f"  about to divide: total={total}  count={count}")  # <-- breakpoint here
    return total / count        # if count is 0 this even crashes


print("Scores:", scores)
result = average(scores)
print("Average:", result)

# ------------------------------------------------------------
# EXPECTED once fixed: (80+90+100)/3 = 90.0
#
# Teaching point: the bug is NOT on the line that crashes
# (the division). The division is just where the bad data
# ARRIVES. The real cause is upstream, where 'count' should
# have changed but never did. Following dataflow means tracing
# a wrong value back to where it was last correct.
# ------------------------------------------------------------
