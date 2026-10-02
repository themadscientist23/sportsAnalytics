export const LEAGUES = {
  nba: { title: 'NBA Teams', hasTies: false },
  nfl: { title: 'NFL Teams', hasTies: true },
  mlb: { title: 'MLB Teams', hasTies: false },
};

export const logoUrl = (league, abbreviation) =>
  `/logos/${league}/${abbreviation}.png`;
