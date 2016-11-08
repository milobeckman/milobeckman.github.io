//////////////////////////////////////////
// 2016 ELECTION RESULT RANDOMIZER      //
// all values measured in HRC minus DJT //
//////////////////////////////////////////

/* @pjs preload="DC-0.png,MD-0.png,VT-0.png,HI-0.png,MA-0.png,CA-0.png,NY-0.png,RI-0.png,IL-0.png,ME1-0.png,WA-0.png,DE-0.png,NJ-0.png,CT-0.png,OR-0.png,ME-0.png,NM-0.png,MN-0.png,VA-0.png,WI-0.png,MI-0.png,PA-0.png,CO-0.png,NH-0.png,NV-0.png,NC-0.png,FL-0.png,ME2-0.png,OH-0.png,AZ-0.png,IA-0.png,NE2-0.png,GA-0.png,SC-0.png,AK-0.png,TX-0.png,MO-0.png,UT-0.png,IN-0.png,TN-0.png,KS-0.png,MS-0.png,MT-0.png,LA-0.png,SD-0.png,NE1-0.png,KY-0.png,AR-0.png,NE-0.png,ID-0.png,AL-0.png,ND-0.png,OK-0.png,WV-0.png,WY-0.png,NE3-0.png,DC-1.png,MD-1.png,VT-1.png,HI-1.png,MA-1.png,CA-1.png,NY-1.png,RI-1.png,IL-1.png,ME1-1.png,WA-1.png,DE-1.png,NJ-1.png,CT-1.png,OR-1.png,ME-1.png,NM-1.png,MN-1.png,VA-1.png,WI-1.png,MI-1.png,PA-1.png,CO-1.png,NH-1.png,NV-1.png,NC-1.png,FL-1.png,ME2-1.png,OH-1.png,AZ-1.png,IA-1.png,NE2-1.png,GA-1.png,SC-1.png,AK-1.png,TX-1.png,MO-1.png,UT-1.png,IN-1.png,TN-1.png,KS-1.png,MS-1.png,MT-1.png,LA-1.png,SD-1.png,NE1-1.png,KY-1.png,AR-1.png,NE-1.png,ID-1.png,AL-1.png,ND-1.png,OK-1.png,WV-1.png,WY-1.png,NE3-1.png,UT-2.png,goalpost.png"; */



float natl_stdev = 3.6;
float northeast_stdev = 2;
float midwest_stdev = 3;
float west_stdev = 3;
float south_stdev = 2.2;

PFont pts_font = createFont("asdf", 10);
PFont headline_font = createFont("Georgia-BoldItalic", 75);
PFont subheadline_font = createFont("Georgia-BoldItalic", 32);

String[] states = {
  "DC", "MD", "VT", "HI", "MA", "CA", "NY", "RI", "IL", "ME1", "WA", "DE", "NJ", "CT", "OR", "ME", "NM", "MN", "VA", "WI", "MI", "PA", "CO", "NH", "NV", "NC", "FL", "ME2", "OH", "AZ", "IA", "NE2", "GA", "SC", "AK", "TX", "MO", "UT", "IN", "TN", "KS", "MS", "MT", "LA", "SD", "NE1", "KY", "AR", "NE", "ID", "AL", "ND", "OK", "WV", "WY", "NE3"
};
int[] evs_array = {
  3, 10, 3, 4, 11, 55, 29, 4, 20, 1, 12, 3, 14, 7, 7, 2, 5, 10, 13, 10, 16, 20, 9, 4, 6, 15, 29, 1, 18, 11, 6, 1, 16, 9, 3, 38, 10, 6, 11, 11, 6, 6, 3, 8, 3, 1, 8, 6, 2, 4, 9, 3, 7, 5, 3, 1
};
int[] evs = new int[states.length];


float[] exps = new float[states.length];
float[] stdevs = new float[states.length];
float[] results = new float[states.length];
int[] winner = new int[states.length];          // 0=HRC, 1=DJT, 2=McM


int clinton_score;
int trump_score;
int mcmullin_score;

int time_counter;




void gen_results() {
  // start with baseline from polls
  float[] exps_array = {
    70.6, 26.4, 26.2, 24.3, 22.3, 22.2, 19.0, 13.2, 12.6, 12.5, 12.1, 12.0, 11.3, 10.9, 8.5, 6.0, 5.5, 5.0, 4.9, 4.2, 4.0, 3.4, 3.2, 1.9, -0.2, -0.2, -0.2, -1.1, -2.3, -3.5, -3.5, -4.2, -4.8, -7.1, -7.6, -9.7, -11.2, -11.3, -12.1, -13.3, -13.4, -15.1, -16.1, -16.6, -17.1, -17.7, -19.0, -20.0, -20.1, -21.3, -22.0, -23.7, -27.1, -27.4, -37.2, -38.5
  };
  for (int i = 0; i < states.length; i++)
    exps[i] = exps_array[i];

  // adjust for national and regional polling error
  float natl_error = randomGaussian() * natl_stdev;
  float northeast_error = randomGaussian() * northeast_stdev;
  float midwest_error = randomGaussian() * midwest_stdev;
  float west_error = randomGaussian() * west_stdev;
  float south_error = randomGaussian() * south_stdev;

  String[] northeast = {
    15, 9, 27, 23, 21, 6, 12, 1, 4, 2, 13, 11, 7
  };
  String[] midwest = {
    28, 20, 19, 17, 30
  };
  String[] west = {
    22, 24, 29, 5, 14, 10
  };
  String[] south = {
    18, 25, 32, 26, 33, 43, 41, 50
  };

  for (int i = 0; i < northeast.length; i++)
    exps[northeast[i]] = exps[northeast[i]] + northeast_error;
  for (int i = 0; i < midwest.length; i++)
    exps[midwest[i]] = exps[midwest[i]] + midwest_error;
  for (int i = 0; i < west.length; i++)
    exps[west[i]] = exps[west[i]] + west_error;
  for (int i = 0; i < south.length; i++)
    exps[south[i]] = exps[south[i]] + south_error;
  for (int i = 0; i < states.length; i++)
    exps[i] = exps[i] + natl_error;

  // adjust for state polling error
  float[] stdevs_array = {
    7.2, 6.8, 11.2, 10, 6.6, 6.0, 6.0, 9.9, 6.0, 10.3, 6.6, 9.5, 6.5, 7, 6.8, 8.4, 7.1, 6.6, 6.2, 6.4, 6.3, 6.3, 6.5, 7.7, 6.7, 6.0, 6.0, 11.6, 6.3, 6.9, 7.1, 13.3, 6.0, 6.0, 11.5, 6.0, 6.0, 6.7, 6.0, 6.3, 6.4, 6.3, 9.0, 5.7, 10.0, 13.0, 5.8, 6.4, 8.1, 7.2, 6.5, 10.3, 6.5, 8.0, 12.5, 11.8
  };
  // i made these too high oops (fixed below)
  for (int i = 0; i < stdevs_array.length; i++)
    stdevs_array[i] = stdevs_array[i] * 0.8;
  for (int i = 0; i < states.length; i++)
    stdevs[i] = stdevs_array[i];

  for (int i = 0; i < northeast.length; i++)
    stdevs[northeast[i]] = sqrt(pow(stdevs[northeast[i]], 2) - pow(northeast_stdev, 2));
  for (int i = 0; i < midwest.length; i++)
    stdevs[midwest[i]] = sqrt(pow(stdevs[midwest[i]], 2) - pow(midwest_stdev, 2));
  for (int i = 0; i < west.length; i++)
    stdevs[west[i]] = sqrt(pow(stdevs[west[i]], 2) - pow(west_stdev, 2));
  for (int i = 0; i < south.length; i++)
    stdevs[south[i]] = sqrt(pow(stdevs[south[i]], 2) - pow(south_stdev, 2));
  for (int i = 0; i < states.length; i++)
    stdevs[states[i]] = sqrt(pow(stdevs[states[i]], 2) - pow(natl_stdev, 2));

  // generate the final results!
  for (int i = 0; i < states.length; i++) {
    results[i] = exps[i] + stdevs[i]*randomGaussian();
    if (results[i] > 0)
      winner[i] = 0;
    else
      winner[i] = 1;
  }

  // UTAH
  if (random(1) < 0.12)
    winner[37] = 2;

  // MAINE & NEBRASKA
  if (winner[9] == winner[27])
    winner[15] = winner[9];
  if (winner[45] == winner[31])
    winner[48] = winner[45];

  // reset the electoral votes
  clinton_score = 0;
  trump_score = 0;
  mcmullin_score = 0;
}

void update_map() {
  String[] ET = {
    15, 23, 2, 4, 6, 7, 13, 12, 21, 11, 1, 18, 53, 28, 20, 25, 33, 32, 26, 9, 27, 0
  };
  String[] CT = {
    50, 39, 41, 46, 38, 8, 19, 17, 30, 36, 47, 43, 35, 52, 40, 48, 45, 31, 55
  };
  String[] MT = {
    51, 44, 42, 54, 22, 16, 37, 29, 49
  };
  String[] PT = {
    10, 14, 24, 5, 34, 3
  };

  if (time_counter == 1) {
    show_states(ET);
    update_score_bar();
  }
  if (time_counter == 20) {
    show_states(CT);
    update_score_bar();
  }
  if (time_counter == 60) {
    show_states(MT);
    update_score_bar();
  }
  if (time_counter == 110) {
    show_states(PT);
    update_score_bar();
    write_headlines();
  }
}

void update_score_bar() {
  textFont(pts_font);
  strokeWeight(3);
  
  // under bar
  stroke(#eeeeee);
  fill(#eeeeee);
  rect(20, 270, 918, 30);
  // clear text
  stroke(#ffffff);
  fill(#ffffff);
  rect(20, 250, 918, 20);

  // clinton bar
  stroke(#1D4780);
  fill(#1D4780);
  float c_len = (float(clinton_score) / 538.0) * 918.0;
  rect(20, 270, c_len, 30);
  
  textAlign(LEFT);
  textSize(20);
  text(clinton_score,25,265);

  // trump bar
  stroke(#BD1B26);
  fill(#BD1B26);
  float t_len = (float(trump_score) / 538.0) * 918.0;
  rect(938-t_len, 270, t_len, 30);
  
  textAlign(RIGHT);
  textSize(20);
  text(trump_score,933,265);
  
  // mcmullin bar
  if (mcmullin_score > 0) {
    stroke(#FFCC00);
    fill(#FFCC00);
    float m_len = (float(mcmullin_score) / 538.0) * 918.0;
    rect(938-t_len-m_len, 270, m_len, 30);
  }
  
  // goalpost
  PImage img = loadImage("randomizer-assets/goalpost.png");
  image(img,0,220);
}

void write_headlines() {
  
  String headline = "error";
  String subh1 = "error";
  String subh2 = "error";
 
  if (clinton_score > 269) {
    headline = "MADAM PRESIDENT";
    
    if (clinton_score > 426)
      subh1 = "CLINTON SECURES WIDEST WIN SINCE REAGAN;";
    else if (clinton_score > 380)
      subh1 = "CLINTON MAKES HISTORY IN LANDSLIDE WIN;";
    else if (clinton_score > 330)
      subh1 = "CLINTON MAKES HISTORY IN DECISIVE WIN;";
    else if (clinton_score > 290)
      subh1 = "GRUELING CAMPAIGN ENDS IN CLINTON WIN;";
    else
      subh1 = "CLINTON MAKES HISTORY WITH NARROW WIN;";
    
    float seed = random(1);
    
    if (seed < 0.4)
      subh2 = "NATION AWAITS CONCESSION FROM TRUMP";
    else if (seed < 0.6)
      subh2 = "TRUMP CRIES “RIGGED” IN RAMBLING SPEECH";
    else if (seed < 0.8)
      subh2 = "DEFLATED TRUMP GIVES BRIEF CONCESSION";
    else
      subh2 = "RIOTS BREAK OUT AS TRUMP CONCEDES RACE";
    
    if winner[37] == 2
      subh2 = "EVAN McMULLIN TAKES UTAH IN LATE SURGE";
    if winner[35] == 0
      subh2 = "RECORD HISPANIC TURNOUT PAINTS TEXAS BLUE";
    
  }
  
  else if (trump_score > 269) {
    headline = "TRUMP PREVAILS";
    
    if (trump_score > 320)
      subh1 = "CLINTON BASE CRUMBLES IN SHOCKING ROUT;";
    else if (trump_score > 290)
      subh1 = "UPSET VICTORY CAUSES GLOBAL SHOCKWAVES;";
    else {
      float seed = random(1);
      
      if (seed < 0.4) {
        subh1 = "IN NARROW WIN, BILLIONAIRE COMPLETES";
        subh2 = "HOSTILE TAKEOVER OF U.S. GOVERNMENT";
      }
      
      else {
        subh1 = "CLINTON, WINNING POPULAR VOTE, FAILS TO";
        subh2 = "CONVERT POLLS IN CRUCIAL SWING STATES";
      }
    }
    
    if (subh2.equals("error")) {
      float seed = random(1);
     
      if (seed < 0.2)
        subh2 = "“SHY TRUMP” VOTERS DEFY EXPECTATIONS";
      else if (seed < 0.4)
        subh2 = "YOUNG VOTERS FAIL TO MATCH OBAMA TURNOUT";
      else if (seed < 0.6)
        subh2 = "VIOLENCE ERUPTS ON ELECTION RESULTS";
      else if (seed < 0.8)
        subh2 = "TRUMP EBULLIENT IN GLOATING SPEECH";
      else
        subh2 = "HIGHEST GENDER BARRIER REMAINS INTACT";
    }
    
  }
  else if (mcmullin_score > 0) {
    headline = "ELECTION DEADLOCK";
    
    subh1 = "McMULLIN WIN IN UTAH PROLONGS ELECTION;";
    subh2 = "HOUSE TO CALL RACE FOR FIRST TIME SINCE 1824";
  }
  else {
    headline = "IT'S A TIE!";
    
    subh1 = "NATION PLUNGES INTO CHAOS ON 269-269 TALLY;";
    subh2 = "HOUSE TO CALL RACE FOR FIRST TIME SINCE 1824";
  }
    
  // draw headline
  fill(#000000);
  textFont(headline_font);
  textAlign(CENTER);
  text(headline,479,80);
  
  // draw line
  strokeWeight(5);
  stroke(#000000);
  line(279,114,679,114);
  
  // draw subhS
  fill(#000000);
  textFont(subheadline_font);
  textAlign(CENTER);
  text(subh1,459,170);
  text(subh2,499,215);
}

void show_states(String[] zone) {
  for (int i = 0; i < zone.length; i++) {
    String img_str = "randomizer-assets/" + states[zone[i]] + "-" + winner[zone[i]] + ".png";
    PImage img = loadImage(img_str);
    image(img, 0, 300);

    if (winner[zone[i]] == 0)
      clinton_score += evs[zone[i]];
    if (winner[zone[i]] == 1)
      trump_score += evs[zone[i]];
    if (winner[zone[i]] == 2)
      mcmullin_score += evs[zone[i]];
  }
}
/*
void run_litmus_tests() {
  int N = 10000;

  IntDict hrc_win_count = new IntDict();
  for (int i = 0; i < states.length; i++)
    hrc_win_count.set(states[i], 0);
  hrc_win_count.set("electoral college", 0);
  hrc_win_count.set("popular vote", 0);

  String x_state = "NC";
  String y_state = "GA";
  float[] x_array = new float[N];
  float[] y_array = new float[N]; 

  // roll the dice
  for (int j = 0; j < N; j++) {
    gen_results();

    for (int i = 0; i < states.length; i++) {
      if (winner.get(states[i]) == 0)
        hrc_win_count.set(states[i], hrc_win_count.get(states[i]) + 1);

      if (states[i].equals(x_state))
        x_array[j] = results.get(states[i]);
      if (states[i].equals(y_state))
        y_array[j] = results.get(states[i]);
    }

    if (clinton_score > 270)
      hrc_win_count.set("electoral college", hrc_win_count.get("electoral college") + 1);
  }

  for (int i = 0; i < states.length; i++) {
    println(states[i] + "\t" + str(float(hrc_win_count.get(states[i]))/N * 100));
  }

  //println("corr btwn " + x_state + " and " + y_state + ": " + str(corr(x_array,y_array)));
  println("EC:" + "\t" + str(float(hrc_win_count.get("electoral college"))/N * 100));
}

float corr(float[] xs, float[] ys) {
  float sx = 0.0;
  float sy = 0.0;
  float sxx = 0.0;
  float syy = 0.0;
  float sxy = 0.0;

  int n = xs.length;

  for (int i = 0; i < n; ++i) {
    float x = xs[i];
    float y = ys[i];

    sx += x;
    sy += y;
    sxx += x * x;
    syy += y * y;
    sxy += x * y;
  }

  // covariation
  float cov = sxy / n - sx * sy / n / n;
  // standard error of x
  float sigmax = sqrt(sxx / n -  sx * sx / n / n);
  // standard error of y
  float sigmay = sqrt(syy / n -  sy * sy / n / n);

  // correlation is just a normalized covariation
  return cov / sigmax / sigmay;
}
*/
void restart() {
  gen_results();
  time_counter = 0;
  background(256, 256, 256);
  update_score_bar();
}

void mouseClicked() {
  restart();
}

void draw() {
  time_counter++;
  update_map();
}

void setup() {
  size(958, 920);
  background(256, 256, 256);
  strokeWeight(0);
  restart();

  for (int i = 0; i < states.length; i++)
    evs[i] = evs_array[i];
}

