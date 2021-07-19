$(function() {
    // REMARK: jQuery вызовет функцию, когда страница прогрузится

    // ********************simple error handling*******************************************

    function onerror(err) {
        var div = $('.err'), p = window.location.protocol, usingHttp = p==='http:' || p==='https:';
		
        $('[data-http='+usingHttp+']', div)
                .removeClass('hide')               //Показать сообщение ошибки, удалив класс
                .find('em').text(err || '(none)'); // Загрузить инормацию об ошибке
        $('main h1').after(div.removeClass('hide')); // Поместить информацию оь ошибке после h1
    }

    // Подгрузка файла CSV с последующим вызовом функции main и отлов ошибок
    try {
        d3.csv('medicines.csv', function(xhr, data) {
            if (!data) return onerror(xhr.statusText);
            main(data);
        }); 
    } catch (err) { onerror(err.message); }
   // ********************End simple error handling*******************************************
   
    var tableTemplate = $([
        "<table class='table table-hover table-condensed table-striped'>",
        "  <caption></caption>",      
        "  <thead><tr/></thead>",
        "  <tbody></tbody>",
        "</table>"
    ].join('\n'));
	
    CreateTable = function(data,variablesInTable,title){
        var table = tableTemplate.clone();
        var ths = variablesInTable.map(function(v) { return $("<th>").text(v) });
        $('caption', table).text(title);
        $('thead tr', table).append(ths);
        data.forEach(function(row) {
            var tr = $("<tr>").appendTo($('tbody', table));
            variablesInTable.forEach(function(varName) {
                // example:  varName = 'value.stockAvg' 
                //           -> keys = [ 'value', 'stockAvg' ]
                //           -> val = row['value']['stockAvg']    
                var val = row, keys = varName.split('.'); 
                keys.forEach(function(key) { val = val[key] });
                tr.append($("<td>").text(val));
            });
        });
        return table;
    }

    main = function(inputdata){ 
        //Our  data: Обычно эта информация вытаскивается с ервера, но сейчас мы читаем ее с локальгого .csv файла
        var medicineData = inputdata;
	
        // Приводим дату к нужному формату
        var dateFormat = d3.time.format("%d/%m/%Y");
        medicineData.forEach(function (d) {
            d.Day = dateFormat.parse(d.Date);     
        })
	
        // Помещаем данные по таблицы в массив, чтобы потом можно было удобно итерировать по ним
        var variablesInTable = ['MedName','StockIn','StockOut','Stock','Date','LightSen']
        // Показываем первые 5 результатов 
        var sample = medicineData.slice(0,5);
        // Создаем таблицу
        var inputTable = $("#inputtable");
        inputTable
                .empty()
                .append(CreateTable(sample,variablesInTable,"Таблица входных данных"));
	
        //************************************************
        //  Adding Crossfilter.js
        //************************************************

        //Initialize a Crossfilter instance
        CrossfilterInstance = crossfilter(medicineData);
	
        // Создаем первое измерение: Имена препаратов 
        var medNameDim = CrossfilterInstance.dimension(function(d) {return d.MedName;});
	
        //    ФИЛЬТРУЕМ ЗНАЧЕНИЯ
	
        var dataFiltered= medNameDim.filter('Grazax 75 000 SQ-T')
        // Показываем отфильтрованные данные
        var filteredTable = $('#filteredtable');
        filteredTable
                .empty()
                .append(CreateTable(dataFiltered.top(5),variablesInTable,'Отфильтрованные данные по имени'));
        //	Создаем измерение по Дате
        var DateDim = CrossfilterInstance.dimension(function(d) {return d.Day;});
        //  Сортируем по Дате, вместо сортировки по имени
        filteredTable
                .empty()
                .append(CreateTable(DateDim.bottom(5),variablesInTable,'Отфильтрованные данные по дате'));
        
        //   MAPREDUCE   
        //reduce count
        var countPerMed = medNameDim.group().reduceCount();
        variablesInTable = ["key","value"]
        filteredTable
                .empty()
                .append(CreateTable(countPerMed.top(Infinity),variablesInTable,'Сжатая таблица'));
	  
        // Наша Reduce функция использует 3 компонента: функции инициализации, добавления и удаления
        // Функция инициализации, задающая начальные значения p-объекта
        var reduceInitAvg = function(p,v){
            return {count: 0, stockSum : 0, stockAvg:0};
        }
        // Функция, которая вызвается при добавлении записи
        var reduceAddAvg = function(p,v){
            p.count += 1;
            p.stockSum  = p.stockSum  + Number(v.Stock);
            p.stockAvg = Math.round(p.stockSum  / p.count);
            return p;
        }
        //  Функция, которая вызвается при удалении записи
        var reduceRemoveAvg = function(p,v){
            p.count -= 1;
            p.stockSum  = p.stockSum  -  Number(v.Stock);
            p.stockAvg = Math.round(p.stockSum  / p.count);
            return p;
        }
        //.reduce() принимает на вход 3 функции(reduceInitAvg(),reduceAddAvg() and reduceRemoveAvg())
        dataFiltered = medNameDim.group().reduce(reduceAddAvg,reduceRemoveAvg,reduceInitAvg)
        
        // Показать результирующую таблицу
        variablesInTable = ["key","value.stockAvg"]
        filteredTable
                .empty()
                .append(CreateTable(dataFiltered.top(Infinity),variablesInTable,'Сжатая таблица'));
 
        medNameDim.filterAll()
		 
        //************************************************
        //  Adding DC.js
        //************************************************
	  
        //  Данные о запасах с течением времени
        var SummatedStockPerDay = DateDim.group().reduceSum(function(d){return d.Stock;})
        //  The Line Chart
        var minDate = DateDim.bottom(1)[0].Day;
        var maxDate = DateDim.top(1)[0].Day;
        var StockOverTimeLineChart = dc.lineChart("#StockOverTime");
	
        // График годовых поставок
        StockOverTimeLineChart
                .width(null) // null - расположит по достпной ширине контейнера
                .height(400)
                .dimension(DateDim)
                .group(SummatedStockPerDay)
                .x(d3.time.scale().domain([minDate,maxDate]))
                .xAxisLabel("2015 год")
                .yAxisLabel("Склад")
                .margins({left: 60, right: 50, top: 50, bottom: 50})
		
        //   Средний запас по медкаментам
        var AverageStockPerMedicineRowChart = dc.rowChart("#StockPerMedicine"); 
	 
        var AvgStockMedicine =  medNameDim.group().reduce(reduceAddAvg,reduceRemoveAvg,reduceInitAvg); 
        AverageStockPerMedicineRowChart
                .width(null) // null - расположит по достпной ширине контейнера
                .height(1200)
                .dimension(medNameDim)
                .group(AvgStockMedicine)
                .margins({top: 20, left: 10, right: 10, bottom: 20})
                .valueAccessor(function (p) {return p.value.stockAvg;}); 
	
        // Запа по светочувствительным медикаметам
        var lightSenDim = CrossfilterInstance.dimension(function(d) {return d.LightSen;}); 
        var SummatedStockLight =  lightSenDim.group().reduceSum(function(d) {return d.Stock;}); 
	
        var LightSensitiveStockPieChart = dc.pieChart("#LightSensitiveStock");
	
        LightSensitiveStockPieChart
                .width(null) // null - расположит по достпной ширине контейнера
                .height(300)
                .dimension(lightSenDim)
                .radius(90)
                .group(SummatedStockLight)  
        //	resetFilters() сбросит данные dc.js и перерисует графики
        resetFilters = function(){
            StockOverTimeLineChart.filterAll();
            LightSensitiveStockPieChart.filterAll();
            AverageStockPerMedicineRowChart.filterAll();
            dc.redrawAll();
        }
        // Вызываем функцию resetFilters() по нажатии кнопки 
        $('.btn-success').click(resetFilters);

        //Отрисовать графики
        dc.renderAll(); 
    }
})
