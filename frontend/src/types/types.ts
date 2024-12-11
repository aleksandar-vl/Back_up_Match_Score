export interface Tournament {
  id: string
  title: string
  tournament_format: string
  start_date: string
  end_date: string
  current_stage: string
  number_of_teams: number
  director_id: string
}

export interface Request {
  id: string;
  email: string;
  request_type: string;
  status: string;
  request_date: string;
  response_date: string | null;
  admin_id: string | null;
  username: string | null;
}

export interface Player {
  id: string;
  username: string;
  first_name: string;
  last_name: string;
  country: string;
  user_email: string;
  team_name: string;
  team_id: string;
  avatar: string | null;
  game_win_ratio: string;
  current_tournament_title: string | null;
  current_tournament_id: string | null;
}

export interface PrizeCut {
  id: string
  tournament_name: string
  prize_cut: number
  place: number
}

export interface Team {
  id: string
  name: string
}

export interface TeamStats {
  tournaments_played: number
  tournaments_won: number
  tournament_win_loss_ratio: {
    ratio: string
  }
  matches_played: number
  matches_won: number
  match_win_loss_ratio: {
    ratio: string
  }
  most_often_played_opponent: string
  best_opponent: string
  worst_opponent: string
}

export interface Match {
  id: string
  match_format: string
  start_time: string
  is_finished: boolean
  stage: string
  team1_id: string
  team2_id: string
  team1_score: number
  team2_score: number
  team1_name: string
  team2_name: string
  team1_logo: string | null
  team2_logo: string | null
  winner_id: string | null
  tournament_id: string
  tournament_title: string
}

export interface Prize {
  id: string
  place: number
  prize_cut: number
  tournament_id: string
  tournament_name: string
  team_id: string | null
  team_name: string | null
  team_logo: string | null
}

export interface FilterOption {
  text: string
  value: string
}

export interface FilterValuesTournament {
  period: string | null
  status: string | null
  format: string | null
}

export interface FilterValuesMatch {
  stage: string | null
  status: string | null
  team: string | null
}
