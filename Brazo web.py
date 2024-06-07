<!DOCTYPE html>
<html>
	<head lang="en">
		<meta charset="utf-8">
		<title>My first three.js app</title>
		<style>
			body { margin: 0; }
		</style>
		<script src="https://cdn.jsdelivr.net/npm/three@0.126.1/build/three.min.js"></script>
	</head>
	<body>
		
        <div id="arm"></div>
        <h1>ARM</h1>
		<div id="error"></div>

		<div>
			<label>Seleccione el archivo
			<input type="file" id="csvFile" accept=".csv">
			<button onclick="Tama()">Cargar CSV</button></label>
		</div>
        


        <button onclick="led_on()">LED ON</button>
        <button onclick="led_off()">LED OFF</button>
        <button onclick="quit()">QUIT</button>
        <div>
			<label for="">Shoulder:</label>
			<a href=\"?Shoulder=-90"\><button>-90</button></a>
			<a href=\"?Shoulder=-45"\><button>-45</button></a>
			<a href=\"?Shoulder=0"\><button>0</button></a>
			<a href=\"?Shoulder=45"\><button>45</button></a>
			<a href=\"?Shoulder=90"\><button>90</button></a>
		</div> 
		<div>
			<label for="">Elbow:</label>
			<a href=\"?Elbow=-90"\><button>-90</button></a>
			<a href=\"?Elbow=-45"\><button>-45</button></a>
			<a href=\"?Elbow=0"\><button>0</button></a>
			<a href=\"?Elbow=45"\><button>45</button></a>
			<a href=\"?Elbow=90"\><button>90</button></a>
		</div> 
		<div> 
            <label for="rangeInput">Shoulder:</label>
            <input type="range" id="rangeInput" name="rangeInput" min="-45" max="45" onchange="moverShoulder(this.value)">
         
            <label for="rangeInput">Elbow:</label>
            <input type="range" id="rangeInput1" name="rangeInput" min="0" max="180" onchange="moverElbow(this.value)">
         
            <label for="rangeInput">Plat:</label>
            <input type="range" id="rangeInput1" name="rangeInput" min="0" max="360" onchange="moverPlat(this.value)">
        </div>
		<a href=\"?moto=arrib"\><button>⬆</button></a>
		<div> 
            <a href=\"?moto=izq"\><button id="⬅">⬅</button></a>
			<a href=\"?moto=aba"\><button>⬇</button></a>
			<a href=\"?moto=dere"\><button>⮕</button></a>
        </div>
		<a href=\"?entrenar"\><button>ENTRENAR</button></a>
		<div> 
            <a href=\"?Subir"\><button>Subir</button></a>
			<a href=\"?Bajar"\><button>Bajar</button></a>
        </div>

    <script>


		

		

		
		let a1 = 0.3;
		let a2 = 0.5;
		let a3 = 0.5;
		let plat_large = 1;
		let base_L = 0.2;
		let espesor_gen = 0.02;
		let ancho_arm_2 = 0.06;


		
		// Define a point in 3D space
		const point = new THREE.Vector3();

		// Set initial LED color and arm dimensions
		let color_led = 0x00fff0;
		const amarillo= 0x00F2E300;
		const cafe= 0x00A9540E;
		const negro=0x00000000;
		const blanco=0x00FFFFFF;
		const azul_osc =0x00044C80;
		// Set up Three.js scene and camera
		const width = window.innerWidth;
		const height = window.innerHeight*0.85;
		const scene = new THREE.Scene();
		const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
		camera.position.x = 0;
		camera.position.y = 3;
		camera.position.z = 0;
		camera.lookAt(0, 0, 0);
		// Create WebGL renderer and append it to the DOM
		const renderer = new THREE.WebGLRenderer();
		renderer.setSize(width, height);
		const arm_DOM = document.getElementById("arm");
		arm_DOM.appendChild(renderer.domElement);
		
		// Define a small dot for visualization
		let dot = new THREE.BoxGeometry(0.01, 0.01, 0.01);
		
		// error label
		const error_DOM = document.getElementById("error");
		error_DOM.innerHTML = "Error="
		


		// Set up the base of the mechanical arm
		let geometry = new THREE.BoxGeometry(plat_large, plat_large*0.05, plat_large*0.65);
		let material2 = new THREE.MeshBasicMaterial({ color:cafe});
		const plat = new THREE.Mesh(geometry, material2);
		scene.add(plat);
		




		// Motoreductores de las ruedas
		geometry = new THREE.BoxGeometry(0.2, 0.05, 0.15);
		let material = new THREE.MeshBasicMaterial({ color: amarillo });
		let motoReduct1=new THREE.Mesh(geometry,material);
		motoReduct1.translateY(-plat_large*0.05);
		motoReduct1.translateZ((plat_large*0.65)/2);
		plat.add(motoReduct1);


		let motoReduct2=new THREE.Mesh(geometry,material);
		motoReduct2.translateY(-plat_large*0.05);
		motoReduct2.translateZ(-(plat_large*0.65)/2);
		plat.add(motoReduct2);
		

		// Ruedas laterales
		geometry = new THREE.CylinderGeometry( 0.2,0.2,0.2, 32 ); 
		material = new THREE.MeshBasicMaterial( {color: blanco} ); 
		let rueda = new THREE.Mesh( geometry, material );
		rueda.translateZ(0.15/2);
		rueda.rotateX(Math.PI/2);
		motoReduct1.add( rueda);
		
		let rueda2 = new THREE.Mesh( geometry, material );
		rueda2.translateZ(-0.15/2);
		rueda2.rotateX(Math.PI/2);
		motoReduct2.add( rueda2);
		
		
		// Base chiquita
		
		geometry = new THREE.BoxGeometry(base_L, espesor_gen, base_L);
		material = new THREE.MeshBasicMaterial({ color: color_led});
		let base = new THREE.Mesh(geometry, material);
		base.translateY(base_L);
		plat.add(base);



		// Paredes laterales
		
		material = new THREE.MeshBasicMaterial({ color: amarillo});
		geometry = new THREE.BoxGeometry(base_L, a1, espesor_gen);
		let pared1= new THREE.Mesh(geometry, material);
		pared1.translateZ(base_L/2);
		pared1.translateY(espesor_gen);
		base.add(pared1);
		
		let pared2= new THREE.Mesh(geometry, material);
		pared2.translateZ(-base_L/2);
		pared2.translateY(espesor_gen);
		base.add(pared2);
		

		// Vallas frontal y trasera
		geometry = new THREE.BoxGeometry(espesor_gen, a1/2, base_L);
		let valla1= new THREE.Mesh(geometry, material);
		valla1.translateX(base_L/2);
		valla1.translateY(espesor_gen);
		base.add(valla1); 
		
		let valla2= new THREE.Mesh(geometry, material);
		valla2.translateX(-base_L/2);
		valla2.translateY(espesor_gen);
		base.add(valla2); 
		
		
		// Triangulo medio
		geometry = new THREE.BoxGeometry(0.05, 0.25*a1, 0.2);
		material = new THREE.MeshBasicMaterial({ color: blanco});
		let trian = new THREE.Mesh( geometry, material );
		trian.translateY(0.05);
		base.add( trian);
		
		

		// Servos de los lados
		geometry = new THREE.BoxGeometry(0.1, 0.05, 0.05);
		material = new THREE.MeshBasicMaterial({ color: azul_osc});
		let servo1_1 = new THREE.Mesh( geometry, material );
		servo1_1.translateZ(espesor_gen);
		pared1.add( servo1_1);
		
		let servo2_2 = new THREE.Mesh( geometry, material );
		servo2_2.translateZ(-espesor_gen);
		pared2.add( servo2_2);
		
		
		


















		
		/* 
		**********************************
		
		Brazo de a2
		
		**********************************
		*/
		
		material = new THREE.MeshBasicMaterial({ color: color_led});
		
		
		
		
		// Base arm a2 pared 2
		
		
		
        /*
        let shoulder = new THREE.Object3D();
        shoulder.translateY(a1 / 2);
        base.add(shoulder);
		*/
        
        
        let shoulder_neg = new THREE.Object3D();
        shoulder_neg.translateY(a1 / 2);
        shoulder_neg.translateX(-base_L/2);
        pared2.add(shoulder_neg);
		
        let shoulder_pos = new THREE.Object3D();
        shoulder_pos.translateX(base_L/2);
        shoulder_pos.translateY(a1 / 2);
        pared2.add(shoulder_pos);
		
		
		// Brazo pared 2
        
		
		geometry = new THREE.BoxGeometry(ancho_arm_2, a2, espesor_gen);
		material = new THREE.MeshBasicMaterial({ color: color_led});
		let col_neg_2 = new THREE.Mesh( geometry, material );
		
		col_neg_2.translateY((a2/2));
		shoulder_neg.add( col_neg_2);
		
		geometry = new THREE.BoxGeometry(ancho_arm_2, a2, espesor_gen);
		material = new THREE.MeshBasicMaterial({ color: color_led});
		let col_neg_1 = new THREE.Mesh( geometry, material );
		
		col_neg_1.translateY((a2/2));
		shoulder_pos.add( col_neg_1);
		
		
		/*
		let col_pos_2 = new THREE.Mesh( geometry, material );
		col_pos_2.translateX(0.1);
		col_pos_2.translateY(0.05+(a2/2));
		base_arm_a2_pared_2.add( col_pos_2);
		
		*/
		
		// Tope arm a2 pared 2
		
		
        let shoulder_final = new THREE.Object3D();
		shoulder_final.translateY(a2/2);
        col_neg_2.add(shoulder_final);
		
		geometry = new THREE.BoxGeometry(base_L, ancho_arm_2, espesor_gen);
		material = new THREE.MeshBasicMaterial({ color: blanco});
		let tope_arm_a2_pared_2 = new THREE.Mesh( geometry, material );
		tope_arm_a2_pared_2.translateX(base_L/2);
		shoulder_final.add( tope_arm_a2_pared_2);
		
		
		// Brazo pared 1	
		
		// Base arm a2
		
		
		
		
		geometry = new THREE.BoxGeometry(base_L, espesor_gen, espesor_gen);
		material = new THREE.MeshBasicMaterial({ color: negro});
		
		let base_arm_a2_pared_1 = new THREE.Mesh( geometry, material );
		base_arm_a2_pared_1.translateZ(base_L);
		base_arm_a2_pared_1.translateX(-base_L/2);
		shoulder_pos.add( base_arm_a2_pared_1);
		
		let elbow = new THREE.Object3D();
		base_arm_a2_pared_1.add( elbow);
		
		
		// Brazo pared 1
		geometry = new THREE.BoxGeometry(ancho_arm_2, a2/3, espesor_gen);
		
		material = new THREE.MeshBasicMaterial({ color: color_led});
		let col1_1 = new THREE.Mesh( geometry, material );
		elbow.add( col1_1);
		
		// Tope arm a2 pared 1
		
		/*
		let elbow = new THREE.Object3D();
		elbow.translateY(a2 / 2);
		lowerArm.add(elbow);
		*/
		
		let elbow_2 = new THREE.Object3D();
		elbow_2.translateY(a2 / 6);
		col1_1.add( elbow_2);
		
		geometry = new THREE.BoxGeometry(ancho_arm_2, a2, espesor_gen);
		material = new THREE.MeshBasicMaterial({ color: blanco});
		let col1_2 = new THREE.Mesh( geometry, material );
		col1_2.translateY(a2 / 2);
		elbow_2.add( col1_2);
		
		
		let elbow_3 = new THREE.Object3D();
		elbow_3.translateY(a2 / 2);
		col1_2.add( elbow_3);
		
		geometry = new THREE.BoxGeometry(ancho_arm_2, a2/3, espesor_gen);
		material = new THREE.MeshBasicMaterial({ color: color_led});
		let col1_3 = new THREE.Mesh( geometry, material );
		col1_3.translateY(-a2 / 6);
		
		elbow_3.add( col1_3);
		
		
		
        
        
        
        
        
        
        
        
        
        
        
        
        
		
        
		
        
        
        
		
		
		
        
		
		/* 
		**********************************
		
		middle trian arm, a2 part
		
		**********************************
		*/
		
		
		// Brazo middle in trian
		
        let shoulder_central = new THREE.Object3D();
        base.add(shoulder_central);
		
		geometry = new THREE.BoxGeometry(ancho_arm_2, a2, base_L/1.5);
		material = new THREE.MeshBasicMaterial({ color: amarillo});
		let col_central_trian = new THREE.Mesh( geometry, material );
		//col_central_trian.translateX(-base_L/2);
		//col_central_trian.translateZ(base_L/2);
		//col_central_trian.rotate(Math.PI/2);
		col_central_trian.translateY(a2/2);
		shoulder_central.add( col_central_trian);
		
        
        
        
		/* 
		**********************************
		
		arm a3  
		
		**********************************
		*/
        
        
        
		// Arm a3 pared 1
		geometry = new THREE.BoxGeometry(a3, ancho_arm_2, espesor_gen);
		material = new THREE.MeshBasicMaterial({ color: amarillo});
		let arm_a3_pared_1 = new THREE.Mesh( geometry, material );
		arm_a3_pared_1.rotateZ(Math.PI/2);
		arm_a3_pared_1.translateX(-a3/2);
		col1_3.add( arm_a3_pared_1);
		
        
		// Arm a3 pared 2
		geometry = new THREE.BoxGeometry(a3, ancho_arm_2, espesor_gen);
		material = new THREE.MeshBasicMaterial({ color: amarillo});
		let arm_a3_pared_2 = new THREE.Mesh( geometry, material );
		arm_a3_pared_2.translateY(-a3/2-0.01);
		arm_a3_pared_2.translateZ(-base_L);
		arm_a3_pared_2.translateX(base_L/2-2*ancho_arm_2);
		arm_a3_pared_2.rotateZ(-Math.PI/2);
		col1_3.add( arm_a3_pared_2);
		
        
        // Tope doble del arm a3
		
		
        let wrist = new THREE.Object3D();
		wrist.translateX(-a3/2);
		wrist.translateZ(-base_L/2);
        arm_a3_pared_1.add(wrist);
        
        
        
        geometry = new THREE.BoxGeometry(espesor_gen, espesor_gen, base_L);
        material = new THREE.MeshBasicMaterial({ color: blanco});
        let tope_arm_a3 = new THREE.Mesh( geometry, material );
        wrist.add( tope_arm_a3);
        
        /* 
        **********************************
        
        arm a3  
        
        **********************************
        */
		
       
       
       
       
       
        
        
        
        
		
		
		material = new THREE.MeshBasicMaterial({ color: color_led});
		
		// Create a hand at the end of the arm
		geometry = new THREE.TorusGeometry(0.1, 0.01, 3, 9, 5.6);
		let hand = new THREE.Mesh(geometry, material);
        hand.translateZ(0.1)
        hand.translateY(-0.1)
		hand.rotation.y = Math.PI / 2;
		hand.rotation.x = 2*Math.PI;
		hand.rotation.z = -Math.PI/2;
		wrist.add(hand);
        
		// Set up parameters for a line to visualize the arm trajectory
		const MAX_POINTS = 1000;
		material = new THREE.LineBasicMaterial({ color: 0x0000ff });
		geometry = new THREE.BufferGeometry();
		const positions = new Float32Array(MAX_POINTS * 3);
		let last_point = 0;
        
		// Set initial positions for the arm trajectory line
		geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
		const line = new THREE.Line(geometry, material);
		scene.add(line);
        
		// Define two points for the Bezier curve
		const P0 = new THREE.Vector3(a2, a1 / 2, -a3);
		const P1 = new THREE.Vector3(a2, a1 / 2, a3);
		var t = 0;

		var P0_camara = new THREE.Vector3(0, 5, 0);
		var P1_camara = new THREE.Vector3(0, 0, 5);
		var t_camara=0
		animate()
		
        
		// Start the animation loop
		
        
		function  animate(){
			
            
            //if (t <= 1) {
                requestAnimationFrame(animate);
                //}
                
                // Calculate inverse kinematics and update arm positions
                let th1p, th2p, th3p, R;
                R = bezier2(P0, P1, t);
                [th1p, th2p, th3p] = inv_kin(R);
                // Loop through the Bezier curve parameter
                if (t <= 1) {
                    t = t + 0.01;
                }
                
                
                /*
                base.rotation.y = th1p;
                shoulder.rotation.z = Math.PI / 2 + th2p;
                elbow.rotation.z = th3p;
                */


                // Visualize the position of the wrist with a dot
                let dot_i = new THREE.Mesh(dot, material);
                wrist.getWorldPosition(point);
                scene.add(dot_i);
                
                // Update the arm trajectory line
                positions[last_point] = point.x;
                positions[last_point + 1] = point.y;
                positions[last_point + 2] = point.z;
                last_point = last_point + 3;
                line.geometry.attributes.position.needsUpdate = true;
                error_DOM.innerHTML = "Error="+R.distanceTo(point)
                
                R_camara = bezier2(P0_camara, P1_camara, t_camara);
                camera.position.set(R_camara.x,R_camara.y,R_camara.z)
                //console.log(camera.position)
                camera.lookAt(0, 0, 0)
                if (t_camara <= 1) {
                    t_camara = t_camara + 0.00033;
                }
                else {
                    t_camara = 0
			}
            
			// Render the scene
			renderer.render(scene, camera);
            
            
            

		}

        function agregarOReemplazarParametroURL(parametro, valor) {
			var url = window.location.href;

			// Verificar si la URL ya tiene parámetros
			if (url.indexOf('?') !== -1) {
				// Si ya tiene parámetros, eliminarlos
				url = url.split('?')[0];
			}

			// Agregar el nuevo parámetro al final
			url += '?' + encodeURIComponent(parametro) + '=' + encodeURIComponent(valor);

			// Actualizar la URL en la barra de direcciones del navegador
			window.history.replaceState(null, null, url);
		}
        
        function moverShoulder (angle) {


            console.log("Ángulo seleccionado:", angle);
            agregarOReemplazarParametroURL("Shoulder", angle)
            shoulder_pos.rotation.z = angle*Math.PI/180;
            shoulder_neg.rotation.z = angle*Math.PI/180;
            shoulder_final.rotation.z = -angle*Math.PI/180;
            shoulder_central.rotation.z = angle*Math.PI/180;
            // Esta función puede realizar acciones basadas en el ángulo seleccionado
            // Por ejemplo, puedes actualizar algún elemento en la página con este valor
        }
        
        function moverElbow (angle) {
            console.log("Ángulo seleccionado:", angle);
			agregarOReemplazarParametroURL("Elbow", angle)
            
            elbow.rotation.z = angle*Math.PI/180;
            elbow_3.rotation.z = angle*Math.PI/180;
            elbow_2.rotation.z = -angle*Math.PI/180;
            // Esta función puede realizar acciones basadas en el ángulo seleccionado
            // Por ejemplo, puedes actualizar algún elemento en la página con este valor
        }
       
		
        function moverPlat (angle) {
            console.log("Ángulo seleccionado:", angle);
			agregarOReemplazarParametroURL("Plat", angle)
            
            plat.rotation.y = angle*Math.PI/180;
            // Esta función puede realizar acciones basadas en el ángulo seleccionado
            // Por ejemplo, puedes actualizar algún elemento en la página con este valor
        }
       
		
		function Tama() {
    	const fileInput = document.getElementById('csvFile');
		const file = fileInput.files[0];
		const reader = new FileReader();

		reader.onload = function(e) {
			const contents = e.target.result;
			const lines = contents.split(/\r?\n|\r/);
			const data = [];

			lines.forEach(line => {
				const values = line.split(';');
				data.push(values);
			});
			
			console.log(data);
			a1=parseFloat(data[0][1]);
			a2 =parseFloat(data[1][1]);
			a3 =parseFloat(data[2][1]);
			plat_large =parseFloat(data[3][1]); 
			base_L =parseFloat(data[4][1]); 
			espesor_gen =parseFloat(data[5][1]); 
			ancho_arm_2 =parseFloat(data[6][1]);
			};

		reader.readAsText(file);
		}
		
	
		
		// Function to turn the LED on
		function led_on() {
            material.color.setRGB(1, 1, 1);
		}

		// Function to turn the LED off
		function led_off() {
			material.color.setRGB(0, 0, 1);
		}

		// Function to quit or reset
		function quit() {
			material.color.setRGB(0, 0, 0);
		}

		// Function to calculate inverse kinematics
		function inv_kin(P) {
			const x03 = -P.x;
			const z03 = P.y;
			const y03 = P.z;
			const th1 = Math.atan2(y03, x03);
			const r1 = Math.sqrt(x03 ** 2 + y03 ** 2);
			const r2 = -(z03 - a1);
			const phi2 = Math.atan2(r2, r1);
			const r3 = Math.sqrt(r1 ** 2 + r2 ** 2);
			const phi1 = Math.acos((a3 ** 2 - a2 ** 2 - r3 ** 2) / (-2 * a2 * r3));
			const th2 = phi2 - phi1;
			const phi3 = Math.acos((r3 ** 2 - a2 ** 2 - a3 ** 2) / (-2 * a2 * a3));
			const th3 = Math.PI - phi3;
			return [th1, th2, th3];
		}

		// Function for Bezier interpolation between two points
		function bezier2(P0, P1, t) {
			const R = P0.clone().multiplyScalar(1 - t).add(P1.clone().multiplyScalar(t));
			return R;
		}
		
		</script>

	</body>
</html>