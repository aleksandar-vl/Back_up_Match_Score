from enum import Enum


class TournamentFormat(str, Enum):
    SINGLE_ELIMINATION = "single elimination"
    ROUND_ROBIN = "round robin"
    ONE_OFF_MATCH = "one off match"


class MatchFormat(str, Enum):
    MR15 = "MR15"
    MR12 = "MR12"


class Stage(str, Enum):
    GROUP_STAGE = "group stage"  # For Round Robin - MR12
    QUARTER_FINAL = "quarter final"  # For Single Elimination - MR15
    SEMI_FINAL = "semi final"  # For Single Elimination - MR15
    FINAL = "final"  # For all formats - MR15
    FINISHED = "finished"

    def next_stage(self):
        if self == Stage.GROUP_STAGE:
            return Stage.FINAL

        if self == Stage.QUARTER_FINAL:
            return Stage.SEMI_FINAL

        if self == Stage.SEMI_FINAL:
            return Stage.FINAL

        if self == Stage.FINAL:
            return Stage.FINISHED

        return Stage.FINISHED


class Role(str, Enum):
    ADMIN = "admin"
    PLAYER = "player"
    DIRECTOR = "director"
    USER = "user"


class RequestStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class RequestType(str, Enum):
    LINK_USER_TO_PLAYER = "link user to player"
    PROMOTE_USER_TO_DIRECTOR = "promote user to director"
