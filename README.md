# st_QWBr_Nma_tools

## Alpha in WordQuant Platform
 
 [Operation](https://platform.worldquantbrain.com/learn/data-and-operators/operators?_gl=1*je5iyn*_ga*MTAwMTk0NzY2OS4xNjcyNzA5NzU3*_ga_9RN6WVT1K1*MTY3MzM2MDU0OC4zNi4xLjE2NzMzNjQ3MjQuNTkuMC4w)

## Note
 1. Setting
- Region
- Universe: top n cổ phiếu có tính thanh khoảng (liquid) cao nhất thị trường
- Delay
	+ 0: dùng n điểm (cả ngày hôm nay) dự đoán hôm nay
	+ 1: dùng n điểm (cả ngày hôm nay) dự đoán ngày mai
- Neutralization:
	+ w2w: trung hòa, trung tính hóa chiến lược đầu tư
	+ thị trường có n mã, alpha = (a1, a2, ..., an), a_i thuộc [0,1], sum(a_i) = 1

            alpha1 = (0.2,0.3,0.4,0.1)
            alpha2 = (-0.2,-0.3,0.4,0.1)
	+ ý nghĩa: 
        - đảm bảo danh mục đầu tư gồm cả các mã long và short với ngân quỹ tương đương
	
    Ex: 
		
		Giả sử dự đoán cả 4 mã đều tăng trong tương lai => mua vào đợi cao hơn thì bán (long)
	    => dùng alpha1
		WQ: không được long hết mà phải short nữa
			=> dùng alpha2 theo nghĩa, về độ tăng: m3>m4>m2>m1
			
		sector_tai chinh: ngân hàng (tpbank, agrbank), bảo hiểm (bảo việt, pvi)
		industry_nganhang = 
		indusy_sua
		indystry_đồuống

- Decay:
	
		alpha = sales/debt

		sales = [[2,2,6,4],
				[5,5,6,6],
				[9,2,1,8]]		

		b1: alpha = sales/debt = (5, 3, 0.1, 0.3)
			decay = 0, alpha = f(sales_hqua, debt_hqua)
			decay = 3, alpha = f(sales_avg_3ngay, deb_avg_3ngay)
			decay = 5: số ngày trading trong 1 tuần

		b2: alpha = (5/sum(alpha), 3/sum(alpha), 0,1/sum(alpha), 0.3/sum(alpha))

		b3: neutralize: alpha = (5-avg(alpha),3-avg(alpha),0.1-avg(alpha),0.3-avg(alpha))


- Trancation:

		trancation = t1
		có nghĩa là a_i = t1 if a_i > t1 else ai với mọi i
- Nan Handling: dữ liệu có thể bị thiếu điền nan, thì xử lý như nào

		nan = avg của 5 ngày
		nan  = 0
		so on
