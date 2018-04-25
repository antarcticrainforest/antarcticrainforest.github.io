<!Doctype html>
<HEAD>
   <META NAME="Description" CONTENT="My Monash Website">
   <TITLE>Martin Bergemann</TITLE>
   <link rel="stylesheet" type="text/css" href="css/my_styles.css">
   <link rel="stylesheet" type="text/css" href="css/accordion.css">
   <link rel="stylesheet" type="text/css" href="css/slideshow.css">
   <link rel="stylesheet" type="text/css" href="css/card.css">
   <link rel="stylesheet" type="text/css" href="css/academicons.css">
   <link rel="stylesheet" type="text/css" href="css/sidebar.css">
   <link rel="stylesheet" type="text/css" href="css/modal_images.css">
   <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
   <link rel='stylesheet' href='https://fonts.googleapis.com/css?family=Roboto'>
   <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
   <!--Add icon library -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
</HEAD>

<body>
<script type="text/javascript" src="javascript/wz_tooltip.js"></script>
<script type="text/javascript" src="javascript/accordion.js"></script>
<script type="text/javascript" src="javascript/modal_images.js"></script>
<header>
<div class="slideshow-container">
  <div class="mySlides fade">
    <img src="src/pic/Darwin_1.jpg" style="width:100%">
  </div>

  <div class="mySlides fade">
    <img src="src/pic/Darwin_8.jpg" style="width:100%">
  </div>

  <div class="mySlides fade">
    <img src="src/pic/Darwin_3.jpg" style="width:100%">
  </div>
 <div class="mySlides fade">
    <img src="src/pic/Darwin_4.jpg" style="width:100%">
  </div>
<div class="mySlides fade">
    <img src="src/pic/Darwin_5.jpg" style="width:100%">
  </div>
<div class="mySlides fade">
    <img src="src/pic/Darwin_6.jpg" style="width:100%">
  </div>
<div class="mySlides fade">
    <img src="src/pic/Darwin_7.jpg" style="width:100%">
  </div>
<div class="mySlides fade">
    <img src="src/pic/Darwin_9.jpg" style="width:100%">
  </div>
  <a class="prev" onclick="plusSlides(-1)">&#10094;</a>
  <a class="next" onclick="plusSlides(1)">&#10095;</a>
</div>
<div style="text-align:center">
  <span class="dot" onclick="currentSlide(1)"></span> 
  <span class="dot" onclick="currentSlide(2)"></span> 
  <span class="dot" onclick="currentSlide(3)"></span> 
  <span class="dot" onclick="currentSlide(4)"></span> 
  <span class="dot" onclick="currentSlide(5)"></span> 
  <span class="dot" onclick="currentSlide(6)"></span> 
  <span class="dot" onclick="currentSlide(7)"></span> 
  <span class="dot" onclick="currentSlide(8)"></span> 
</div>
</header>

<script type="text/javascript" src="javascript/slideshow.js"></script>


<nav id="mySidenav" class="sidenav">
       <a href="http://users.monash.edu.au/~bergem"  onmouseover="Tip('Go to the start-page')" onmouseout="UnTip()" id="a">Home:</a>
       <a href="http://users.monash.edu.au/~bergem/index.php?link=cv"  onmouseover="Tip('HTML-Version of my CV')" onmouseout="UnTip()" id="b">CV:</a>
       <a href="http://users.monash.edu.au/~bergem/index.php?link=pub"  onmouseover="Tip('Recent scientific pbulications')" onmouseout="UnTip()" id="c">Publications:</a>
       <a href="http://users.monash.edu.au/~bergem/index.php?link=pro"  onmouseover="Tip('My current projects that I am working on')" onmouseout="UnTip()" id="d">Projects:</a>
       <a href="http://users.monash.edu.au/~bergem/index.php?link=meet"  onmouseover="Tip('Some talks to share with the world')" onmouseout="UnTip()" id="e">Meetings:</a>
       <a href="https://github.com/antarcticrainforest" target=_blank onmouseover="Tip('Check out my Software on GitHub')" onmouseout="UnTip()" id="f">Software:</a>
</nav>



<main role='main'>
<article>

<!--<br><br><br><br><p>-->
<br><p>
    <?php
        $links=array(
            'cv' => 'cv.html',
            'pub' => 'pub.html',
            'pro' => 'pro.html',
            'meet' => 'meet.html',
	    'um_do'=> '.um/index.xhtml'
        );
        $hfile='src/html/home.html';
        if (isset ($_GET['link'])){
            $value=$_GET['link'];
            if (isset ($links[$value])){
              $hfile='src/html/' . $links[$value];
            
            }else{
             $hfile='src/html/no_found.html';
            }
        
        }
        
        $str=file_get_contents($hfile,true);
            echo $str . "\n" ;
    ?>
</p>
</article>
</main>
<footer> 
<a class='link' href="mailto:martin.bergemann@monash.edu" target=_blank onmouseover="Tip('Get in Contact with me')" onmouseout="UnTip()">Contact</a>
<a class='contact'  href="mailto:martin.bergemann@monash.edu" target=_blank onmouseover="Tip('EMail')" onmouseout="UnTip()"><i class="fa fa-paper-plane fa-1x"></i></a> 
<a class='contact'  href="http://orcid.org/0000-0003-0604-4103" target=_blank onmouseover="Tip('OrcId')" onmouseout="UnTip()"><i class="ai ai-orcid ai-1x"></i></a> 
<a class='contact'  href="https://www.researchgate.net/profile/Martin_Bergemann" target=_blank onmouseover="Tip('ResearchGate')" onmouseout="UnTip()"><i class="ai ai-researchgate ai-1x"></i></a> 
<a class='contact' href="https://github.com/antarcticrainforest" target=_blank onmouseover="Tip('My Software on GitHub')" onmouseout="UnTip()"><i class="fa fa-github-alt fa-1x"></i></a> 
<a class='contact' href="https://www.linkedin.com/in/martin-bergemann-3453b9141" target=_blank onmouseover="Tip('LinkedIn')" onmouseout="UnTip()"><i class="fa fa-linkedin fa-1x"></i></a> 
<a class='contact' href="https://scholar.google.com.au/citations?user=rEVoxcQAAAAJ&hl=en" target=_blank onmouseover="Tip('Google Scholar')" onmouseout="UnTip()"><i class="ai ai-google-scholar-square ai-1x"></i></a> 
<p> 2017 Martin Bergemann</p>
</footer>
</body>
</HTML>
